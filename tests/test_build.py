"""Check publication and draft behavior without modifying the real website."""
import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("site_build", SOURCE / "scripts/build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for directory in ("content", "templates"):
            shutil.copytree(SOURCE / directory, self.root / directory)
        # Use only each test's own articles, regardless of real publication state.
        for post in (self.root / "content/posts").rglob("*.md"):
            if not post.stem.startswith("_"):
                post.unlink()
        shutil.copyfile(SOURCE / "styles.css", self.root / "styles.css")
        self.previous = builder.ROOT
        builder.ROOT = self.root

    def tearDown(self):
        builder.ROOT = self.previous
        self.temp.cleanup()

    def post(self, slug, date="2020-01-01", draft="false", body="## Body\n\nA paragraph."):
        path = self.root / "content/posts" / (slug + ".md")
        path.write_text(f'---\ntitle: "{slug}"\ndate: "{date}"\nsummary: "A summary"\nlang: ko\ndraft: {draft}\n---\n\n{body}\n')
        return path

    def build(self, drafts=False):
        with contextlib.redirect_stdout(io.StringIO()):
            builder.build(drafts)

    def translation(self, slug, date="2020-01-01", draft="false"):
        path = self.root / "content/posts/en" / (slug + ".md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'---\ntitle: "An English title"\ndate: "{date}"\nsummary: "An English summary"\nlang: en\ndraft: {draft}\n---\n\n## English heading\n\nAn English paragraph.\n')
        return path

    def test_public_post_reaches_page_list_and_feed(self):
        self.post("a-public-post")
        self.build()
        for filename in ("index.html", "blog/index.html", "blog/a-public-post/index.html", "feed.xml"):
            self.assertIn("a-public-post", (self.root / filename).read_text())
        self.assertIn("<h2>Body</h2>", (self.root / "blog/a-public-post/index.html").read_text())
        self.assertEqual(len(ET.parse(self.root / "feed.xml").findall("./channel/item")), 1)

    def test_drafts_future_posts_and_template_stay_out(self):
        self.post("private-draft", draft="true")
        self.post("future-post", date="2999-01-01")
        self.build()
        self.assertEqual(list((self.root / "blog").glob("*/index.html")), [])
        for name in ("index.html", "blog/index.html", "feed.xml"):
            self.assertNotIn("private-draft", (self.root / name).read_text())
            self.assertNotIn("future-post", (self.root / name).read_text())

    def test_preview_is_labeled_excluded_from_rss_and_removed_on_normal_build(self):
        self.post("a-draft", draft="true")
        self.build(True)
        draft = self.root / "blog/a-draft/index.html"
        self.assertIn("noindex, nofollow", draft.read_text())
        self.assertIn("Local preview", draft.read_text())
        ko_draft = self.root / "ko/blog/a-draft/index.html"
        self.assertIn("로컬 미리보기", ko_draft.read_text())
        self.assertNotIn("a-draft", (self.root / "feed.xml").read_text())
        self.build()
        self.assertFalse(draft.exists())
        self.assertFalse(ko_draft.exists())

    def test_language_switch_and_navigation_preserve_each_page(self):
        self.build()
        for path in ("", "research/", "company/", "project/", "blog/"):
            en = (self.root / path / "index.html").read_text()
            ko = (self.root / "ko" / path / "index.html").read_text()
            self.assertIn('<html lang="en">', en)
            self.assertIn('<html lang="ko">', ko)
            self.assertIn(f'data-language-switch href="/ko/{path}"', en)
            self.assertIn(f'data-language-switch href="/{path}"', ko)
            self.assertIn('href="/ko/research/"', ko)
            self.assertIn('href="/ko/company/"', ko)
            self.assertIn('href="/ko/project/"', ko)
            self.assertIn('href="/ko/blog/"', ko)

    def test_company_and_research_contacts_are_distinct_in_both_languages(self):
        self.build()
        for path in ("index.html", "ko/index.html"):
            page = (self.root / path).read_text()
            self.assertIn('technoking@plaid.ai.kr', page)
            self.assertIn('taewan2002@kaist.ac.kr', page)
            company_section = page.split('id="company"', 1)[1]
            self.assertIn('technoking@plaid.ai.kr', company_section)
            self.assertNotIn('taewan2002@kaist.ac.kr', company_section)

    def test_untranslated_post_falls_back_to_original_without_language_label(self):
        self.post("korean-writing", body="## 원문 제목\n\n원문은 번역하지 않습니다.")
        self.build()
        for path in ("blog/korean-writing/index.html", "ko/blog/korean-writing/index.html"):
            page = (self.root / path).read_text()
            self.assertIn('<div class="prose" lang="ko"><h2>원문 제목</h2>', page)
            self.assertIn('rel="canonical" href="https://taewan2002.github.io/ko/blog/korean-writing/"', page)
            self.assertNotIn('Original text:', page)
            self.assertNotIn('본문 언어:', page)
            self.assertNotIn('hreflang="en"', page)

    def test_translated_post_localizes_content_metadata_lists_and_switches(self):
        self.post("bilingual", body="한국어 본문입니다.")
        self.translation("bilingual")
        self.build()
        for lang, prefix, title, body, summary in (
            ("en", "", "An English title", "An English paragraph.", "An English summary"),
            ("ko", "ko/", "bilingual", "한국어 본문입니다.", "A summary"),
        ):
            page = (self.root / prefix / "blog/bilingual/index.html").read_text()
            self.assertIn(f'<h1 lang="{lang}">{title}</h1>', page)
            self.assertIn(f'<div class="prose" lang="{lang}">', page)
            self.assertIn(body, page)
            self.assertIn(f'<meta name="description" content="{summary}">', page)
            self.assertIn(f'rel="canonical" href="{builder.SITE}/{prefix}blog/bilingual/"', page)
            self.assertIn(f'hreflang="en" href="{builder.SITE}/blog/bilingual/"', page)
            self.assertIn(f'hreflang="ko" href="{builder.SITE}/ko/blog/bilingual/"', page)
            other_prefix = "ko/" if lang == "en" else ""
            self.assertIn(f'data-language-switch href="/{other_prefix}blog/bilingual/"', page)
            for listing in ("index.html", "blog/index.html"):
                content = (self.root / prefix / listing).read_text()
                self.assertIn(f'<span lang="{lang}">{title}</span>', content)
                self.assertEqual(content.count('class="post-item"'), 1)
        self.assertNotIn("한국어 본문입니다.", (self.root / "blog/bilingual/index.html").read_text())
        self.assertNotIn("An English paragraph.", (self.root / "ko/blog/bilingual/index.html").read_text())
        items = ET.parse(self.root / "feed.xml").findall("./channel/item")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].findtext("link"), builder.SITE + "/ko/blog/bilingual/")

    def test_translated_drafts_are_private_and_cleaned_up_together(self):
        self.post("bilingual-draft", draft="true")
        self.translation("bilingual-draft", draft="true")
        self.build(True)
        for prefix in ("", "ko/"):
            page = self.root / prefix / "blog/bilingual-draft/index.html"
            self.assertIn("noindex, nofollow", page.read_text())
        self.assertNotIn("bilingual-draft", (self.root / "feed.xml").read_text())
        self.build()
        for prefix in ("", "ko/"):
            self.assertFalse((self.root / prefix / "blog/bilingual-draft/index.html").exists())
            self.assertNotIn("bilingual-draft", (self.root / prefix / "blog/index.html").read_text())

    def test_translation_cannot_publish_a_draft_original(self):
        self.post("not-ready", draft="true")
        self.translation("not-ready", draft="false")
        with self.assertRaisesRegex(ValueError, "draft state must match"):
            self.build()

    def test_translation_requires_matching_original_date_and_language(self):
        self.translation("orphan")
        with self.assertRaisesRegex(ValueError, "needs an original"):
            self.build()
        self.post("orphan", date="2020-02-01")
        with self.assertRaisesRegex(ValueError, "date and draft state"):
            self.build()
        path = self.translation("orphan", date="2020-02-01")
        path.write_text(path.read_text().replace("lang: en", "lang: ko"))
        with self.assertRaisesRegex(ValueError, "translation language"):
            self.build()

    def test_removing_translation_restores_original_fallback(self):
        self.post("translated-once", body="한국어 원문입니다.")
        path = self.translation("translated-once")
        self.build()
        path.unlink()
        self.build()
        page = (self.root / "blog/translated-once/index.html").read_text()
        self.assertIn("한국어 원문입니다.", page)
        self.assertNotIn("An English paragraph.", page)
        self.assertNotIn('hreflang="en"', page)

    def test_publication_titles_and_urls_stay_original_in_korean(self):
        self.build()
        ko = (self.root / "ko/research/index.html").read_text()
        for paper in builder.read_json("content/publications.json"):
            self.assertIn(builder.esc(paper["title"]), ko)
            self.assertIn(builder.esc(paper["summary_ko"]), ko)
            if paper["url"]:
                self.assertIn('href="' + builder.esc(paper["url"]) + '"', ko)

    def test_home_only_lists_latest_three_posts(self):
        for number in range(1, 5):
            self.post(f"entry-{number}", date=f"2020-01-0{number}")
        self.build()
        home = (self.root / "index.html").read_text()
        self.assertNotIn("/blog/entry-1/", home)
        self.assertLess(home.index("/blog/entry-4/"), home.index("/blog/entry-3/"))
        self.assertIn("/blog/entry-1/", (self.root / "blog/index.html").read_text())

    def test_raw_html_and_script_links_do_not_execute(self):
        self.post("unsafe-content", body='<script>alert(1)</script>\n\n[bad](javascript:alert(1))')
        self.build()
        page = (self.root / "blog/unsafe-content/index.html").read_text()
        self.assertNotIn("<script>alert", page)
        self.assertNotIn('href="javascript:', page)

    def test_local_diagrams_use_mobile_companions_and_keep_alt_text(self):
        asset = self.root / "assets/blog/example/flow-mobile.svg"
        asset.parent.mkdir(parents=True)
        asset.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.post("diagram", body='![A → B](/assets/blog/example/flow.svg)\n\n![Ordinary](/assets/photo.png)')
        self.build()
        page = (self.root / "blog/diagram/index.html").read_text()
        self.assertIn('srcset="/assets/blog/example/flow-mobile.svg"', page)
        self.assertIn('alt="A → B"', page)
        self.assertEqual(page.count('<picture class="article-diagram">'), 1)
        self.assertIn('src="/assets/photo.png"', page)

    def test_article_tables_are_keyboard_accessible_in_both_languages(self):
        table = '| Comparison | Result |\n| --- | --- |\n| Computation | 194 seconds |'
        self.post("table-example", body=table)
        translated = self.translation("table-example")
        translated.write_text(translated.read_text() + '\n' + table + '\n')
        self.build()
        from html.parser import HTMLParser

        class TableRegions(HTMLParser):
            def __init__(self):
                super().__init__()
                self.regions = []
                self.table_count = 0

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if attrs.get('role') == 'region':
                    self.regions.append(attrs)
                if tag == 'table':
                    self.table_count += 1

        for prefix, label in (("", "scroll horizontally"), ("ko/", "가로로 스크롤")):
            page = (self.root / prefix / 'blog/table-example/index.html').read_text()
            parsed = TableRegions()
            parsed.feed(page)
            self.assertEqual(parsed.table_count, 1)
            self.assertEqual(len(parsed.regions), 1)
            self.assertEqual(parsed.regions[0]['tabindex'], '0')
            self.assertIn(label, parsed.regions[0]['aria-label'])
            self.assertIn('<td>194 seconds</td>', page)

    def test_research_figures_have_localized_accessible_descriptions(self):
        self.build()
        en = (self.root / 'research/index.html').read_text()
        ko = (self.root / 'ko/research/index.html').read_text()
        for paper in builder.read_json('content/publications.json'):
            self.assertIn('alt="' + builder.esc(paper['image_alt']) + '"', en)
            self.assertIn('alt="' + builder.esc(paper['image_alt_ko']) + '"', ko)
        self.assertIn('retovla 그림을 원본 크기로 보기', ko)

    def test_invalid_front_matter_does_not_overwrite_existing_site(self):
        self.build()
        before = (self.root / "index.html").read_bytes()
        self.post("broken", draft='"false"')
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(before, (self.root / "index.html").read_bytes())

    def test_generated_cleanup_preserves_handwritten_page(self):
        self.post("to-remove")
        self.build()
        other = self.root / "blog/handwritten/index.html"
        other.parent.mkdir()
        other.write_text("<h1>Keep me</h1>")
        (self.root / "content/posts/to-remove.md").unlink()
        self.build()
        self.assertFalse((self.root / "blog/to-remove/index.html").exists())
        self.assertEqual(other.read_text(), "<h1>Keep me</h1>")


if __name__ == "__main__":
    unittest.main()
