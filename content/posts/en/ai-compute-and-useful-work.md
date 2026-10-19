---
title: "The New Economics of AI Infrastructure and Blockchain"
date: "2026-10-18"
summary: "What if AI GPUs became the ASICs of the PoUW era? Thoughts on AI compute and mining from running my own servers."
lang: en
draft: false
---

Running LLM inference and mining Pearl made me wonder whether the two could share the same computation. If the matrix multiplications that produce a model's answer could also earn mining rewards, those rewards might cover part of the inference bill I am already paying.

That is what interests me about Proof of Useful Work, or PoUW. But replacing conventional mining with matrix multiplication is not enough. The system has to preserve the actual inference result while proving that work was done, and the overhead has to stay small. To understand how Pearl approaches this, I read the research behind it, looked through its GPU kernels, and tested some of the numerical operations myself.

*I mine and hold PRL. This essay reflects my operating experience and reading of public sources. It is not investment advice.*

## Running local models alongside a miner

At Plaid Labs, we built a small AI server with four RTX PRO 6000 Blackwell GPUs before memory supplies tightened. I think relying entirely on subscriptions to frontier models leaves us exposed to changes in pricing, usage limits, and provider policies. Having models we can run ourselves gives us more options over the long term.

We already route some production traffic to local models and use frontier models where the task calls for them. Operating both helps us decide which work belongs where.

One thing running a server teaches you is that throughput and demand are separate problems. Multiplying tokens per second by an API price does not produce revenue unless requests keep arriving at that rate. A miner can run without waiting for a customer. Its rewards depend on token prices and difficulty, and electricity still costs money, but the conditions for earning revenue differ from those of an inference service.

On October 17, [Vitalik Buterin compared the cost structures of mining and AI inference on X](https://x.com/VitalikButerin/status/2111334091354251615). His observation was that Bitcoin mining costs are split roughly evenly between compute capital expenditure and electricity, while AI inference is much more heavily dominated by capital expenditure. He did not mention Pearl or PRL, but the comparison caught my attention as someone operating servers.

When hardware is expensive, serving more real requests on the same server spreads that fixed cost over more work. Bitcoin's cost breakdown cannot simply be applied to GPU mining, but it is a useful prompt to think about utilization. What interests me most is earning a mining reward from the computation of an incoming inference request. That has a different cost structure from alternating between inference and mining or assigning a separate job to an idle GPU.

## How mining works

To understand what PoUW changes, it helps to start with what mining does. A blockchain is a ledger maintained by many participants. New transactions are grouped into blocks and appended to it. Proof of Work (PoW) uses a competition in computation to determine who gets an opportunity to propose the next block. In Bitcoin, the process looks like this:

1. A miner assembles transactions into a candidate block. In a mining pool, the pool usually handles this step.
2. The miner changes fields such as the `nonce` in the block header and repeatedly hashes it. A hash **at or below the target** satisfies the proof-of-work condition.
3. The miner broadcasts the block. If it is valid and remains in the accepted chain, the miner receives newly issued coins and transaction fees. Blocks found at nearly the same time can temporarily create competing branches.
4. Other nodes hash the submitted header to check the proof of work quickly. They must also check transactions and signatures separately. [Bitcoin mining documentation](https://developer.bitcoin.org/devguide/mining.html)

Think of rolling dice and winning whenever the result is at or below a threshold. Any single roll is a matter of luck, but someone who rolls more often wins more often over time. Solo mining can leave long, unpredictable gaps between rewards, so miners often join pools. A pool distributes rewards according to `shares`, which represent contributed work; the exact payment scheme varies by pool.

Difficulty adjusts the average interval between blocks. Bitcoin targets [ten minutes on average](https://developer.bitcoin.org/devguide/block_chain.html), while [Pearl's mainnet code specifies 194 seconds](https://github.com/pearl-research-labs/pearl/blob/master/node/chaincfg/params.go#L357). Neither means that a block arrives at exactly that interval. As total compute grows, difficulty adjusts. If my hardware accounts for a smaller fraction of the network, its expected rewards per unit of time fall.

This competition also makes rewriting transaction history costly. An attacker has to catch up with the existing chain and accumulate more work. A majority of the network's computational power is a powerful condition for sustaining that effort, although a smaller attacker still has some probability of reversing a short stretch of history. Even a majority cannot forge someone else's signature or issue arbitrary amounts of currency. [Proof of work and chain selection](https://developer.bitcoin.org/devguide/block_chain.html) · [Limits on what an attacker can do](https://bitcoin.org/en/faq#could-users-collude-against-bitcoin)

## From CPUs to ASICs, and the alternative of PoS

Because miners benefit from performing more of the same computation at a lower cost, Bitcoin mining hardware quickly became specialized.

| Period | Hardware | What changed |
| --- | --- | --- |
| 2009 | CPU | Early mining on personal computers |
| 2010 | GPU | Parallel hashing brought GPUs into widespread use |
| 2011 | FPGA | Reconfigurable circuits offered better energy efficiency |
| 2013 onward | ASIC | Chips specialized for SHA-256 mining displaced general-purpose hardware |

[Michael B. Taylor's 2013 paper](https://michaeltaylor.org/papers/bitcoin_taylor_cases_2013.pdf) documents this progression. Today, Bitcoin mining depends heavily on hardware efficiency, electricity prices, cooling, and operating scale. Hashing secures the ledger, but its outputs cannot be reused as answers to AI queries or scientific computations. That is the starting point for PoUW.

Ethereum chose a different route. Its [transition to Proof of Stake (PoS) on September 15, 2022](https://ethereum.org/roadmap/merge/) eliminated PoW mining and reduced energy consumption by roughly 99.95%, according to its official estimate. Validators stake ETH to propose and validate blocks, with penalties that can take away stake for violating the rules. This uses much less energy, while making the concentration of stake and validator operators important considerations. [Ethereum's explanation of PoS](https://ethereum.org/developers/docs/consensus-mechanisms/pos/)

## Combining mining with work that already needs to be done

PoUW aims to make proof-of-work computation produce something useful outside the blockchain. It is not limited to AI, but Pearl's chosen workload is matrix multiplication, which is widely used in training and inference. If work we already need can also secure a ledger, the two activities could share some of the costs we would otherwise pay separately.

| Comparison | Bitcoin PoW | Pearl's approach to PoUW |
| --- | --- | --- |
| Main computation | Repeated SHA-256 hashing | Matrix multiplication with added noise and processing of the computation record |
| Use of the result | Blockchain security | Security, with the original matrix product available for use |
| Hardware | SHA-256 ASICs | Supported GPUs used for AI computation |
| Verification | Compare the header hash with the target | Verify the winning condition and a cryptographic proof of the computation record |

A result that could be useful is not necessarily serving a real AI request. I will return to that distinction through my own mining experience.

The design builds on a [paper by Ilan Komargodski and Omri Weinstein](https://arxiv.org/abs/2504.09971), first released in April 2025. It attaches proof of work to a matrix multiplication chosen by the miner. Under the paper's assumptions, the relative computational overhead shrinks as the matrix size grows. That does not mean near-zero overhead on every GPU or in every service. But if rewards exceed the additional costs, there may be room to lower inference prices or improve margins.

In May 2026, Together AI [announced a partnership with Pearl](https://www.together.ai/blog/together-ai-partners-with-pearl-research-labs) and introduced discounted inference endpoints incorporating mining rewards. This does not establish the same economics for every model and GPU, but it is an attempt to build a service in the direction I had been wondering about.

### A mining plugin for vLLM

[Pearl's `vllm-miner`](https://github.com/pearl-research-labs/pearl/blob/master/miner/vllm-miner/README.md) is a public implementation of this integration. vLLM is an engine for serving LLM inference. The Pearl plugin replaces targeted quantized linear operations with mining-enabled `NoisyGEMM` operations, producing mining records from the matrix multiplications used in inference. The vLLM integration is therefore already more than a proposal for future work.

The [official mining documentation](https://github.com/pearl-research-labs/pearl/blob/master/miner/README.md) describes support for mining through vLLM and an interest in future plugins for SGLang, TensorRT-LLM, and Ollama. Its published GPU support and testing guidance currently covers H100/H200 (sm90).

## Attaching proof of work to matrix multiplication

![Matrix-multiplication mining. Low-rank noise is added to the inputs. The final result is corrected to recover the original product, while a record of intermediate values is hashed to check the winning condition. A winning attempt submits a proof and block for verification.](/assets/blog/pearl/pouw-process.svg)

*Figure 1. The required result is recovered from the final output, while intermediate partial sums provide the record used for mining. This conceptual diagram of the integer-based approach omits details such as input commitments and FP8 numerical rules. [PoUW paper](https://arxiv.org/html/2504.09971v4#S2) · [Pearl proof system](https://github.com/pearl-research-labs/pearl#repository-layout).*

Read Figure 1 from top to bottom. `A` and `B` are the matrices we originally wanted to multiply; `E` and `F` are low-rank noise added to them. The `S₁`, `S₂`, … in the middle are **partial sums**, accumulated as small blocks are multiplied. The system records intermediate steps as well as the final result, `C′`.

At the bottom, the same computation feeds two paths. On the left, removing the noise contribution from `C′` recovers the required product, `AB`. On the right, the record of intermediate values, or **transcript**, is hashed and checked against the difficulty target. A winning attempt submits a proof and a block for verification. The result on the left remains useful whether or not the attempt wins. In an inference service, that result must feed the model's next operation.

### Using the computation record rather than just the final answer

Hashing only the final matrix product, `C = AB`, is not enough to establish how much work was done. Miners can choose their inputs. If they choose all-zero matrices, they already know the answer without performing a large matrix multiplication.

The added noise helps address this problem. The relationship between the noisy computation and the original result is:

```text
C′ = (A + E)(B + F)
AB = C′ − AF − E(B + F)
```

When the noise rank is small relative to the matrix dimensions, `AF` and `E(B + F)` can be evaluated through smaller multiplications, reducing the cost of recovering `AB`. These equations describe the basic idea; they do not automatically cancel rounding errors in a floating-point implementation.

Noise alone does not solve the problem. If the original inputs are zero, the product of the noise matrices can also be computed quickly using their low-rank structure. This is why the transcript of intermediate values in a prescribed order matters. The assumption is that a shortcut to the final answer does not necessarily provide an easy shortcut to all those intermediate values. The design's security relies on the computational hardness assumption stated in the paper. [Details of the construction](https://arxiv.org/html/2504.09971v4#S2)

### A fused kernel to reduce extra memory traffic

On a GPU, where those intermediate values live matters. Writing partial sums to off-chip HBM or GDDR memory and reading them back in a separate hashing kernel adds memory traffic and kernel launch costs.

In the public [GEMM mainloop for the existing integer path](https://github.com/pearl-research-labs/pearl/blob/master/miner/pearl-gemm/csrc/gemm/collective_mainloop.hpp), TMA brings input tiles into shared memory, and WGMMA performs the matrix multiplications. The loop also incorporates accumulator values into `hash_accumulator`. This is **kernel fusion**: matrix multiplication and transcript accumulation happen in the same kernel.

![Fused kernel comparison. Separate kernels would write partial sums to off-chip GPU memory and read them back. The fused kernel performs GEMM and transcript accumulation in the same mainloop, reducing extra memory round trips for intermediate values.](/assets/blog/pearl/fused-kernel.svg)

*Figure 2. The separate-kernel path is a hypothetical comparison, not an earlier Pearl implementation. The fused path depicts the core of the [public integer GEMM mainloop](https://github.com/pearl-research-labs/pearl/blob/master/miner/pearl-gemm/csrc/gemm/collective_mainloop.hpp). Input and output transfers, additional computation, and proof-generation costs remain.*

Fusion reduces those extra round trips, but register usage, synchronization, and the preparation and removal of noise still have costs. A fast kernel alone does not tell us how much a serving system will benefit.

Pearl is also optimizing inference kernels themselves. Its [analysis of MoE Grouped GEMM on Blackwell](https://pearlresearch.ai/research/blog/grouped-gemm) compares kernels that group matrix multiplications across experts. In its own benchmarks using `gate/up` operation shapes from MoE models such as GLM-5.3, Pearl reports beating FlashInfer and other implementations. For some small decode workloads, it reports being up to 15% faster than quack, the fastest competing implementation in that comparison.

These are kernel timings, measured inside CUDA Graphs after tuning each implementation. They are not measurements of an entire service with mining and proof generation included. Pearl says it plans to release this Grouped GEMM implementation as part of its FP8 scheme. I am interested in how much these optimizations might reduce the overhead of adding mining to real inference.

### Validators should not have to repeat the full multiplication

If every node had to repeat the miner's large matrix multiplication to check it, verification would become expensive across the network. Pearl uses a ZK proof system for this purpose. Its public repository includes [Plonky2/STARKy-based proof-of-work circuits and verifiers](https://github.com/pearl-research-labs/pearl#repository-layout).

The winning condition determines the opportunity to propose a block; the proof establishes whether the submitted computation record follows the rules. The [public integer implementation](https://github.com/pearl-research-labs/pearl/blob/master/zk-pow/src/v1/api/plain_proof.rs) selects the input rows and columns corresponding to the winning region to construct that proof. Validators check it instead of repeating the entire large matrix multiplication. Generating and verifying proofs still takes time and computation.

The proof covers the inputs and computation record handled by the circuit. It does not certify every output of the entire matrix multiplication, or prove that a full model ran and answered a customer's request.

## Matrix multiplication alone is not enough

I have not yet connected the vLLM mining plugin to our service. The separate miner I currently run multiplies random matrices. It earns rewards, but no customer is waiting for its output. That is different from the public inference integration described above.

Curious about what other participants were computing, I also examined proofs from 300 recent blocks. I could see various matrix dimensions, but I could not identify which model or request those operations belonged to. That means I could not establish their use; it is not evidence that no real AI computation was happening.

Since then, I have been more careful with the phrase “useful computation.” The version of PoUW I want to see connects a matrix multiplication to a particular model, input, and output, with someone who actually needs that output. Rewards may attract hardware and developers first. After that, I want to know how much real demand those machines serve.

## Why I am watching FP8

FP8 represents numbers in an 8-bit floating-point format. On supported GPUs, it can reduce data movement and take advantage of fast Tensor Core operations. Sharing computation between inference and mining also requires compatible numerical formats, which is why I have been following Pearl's FP8 work.

When I checked on October 18, 2026, [FP8 mining implementation PR #311](https://github.com/pearl-research-labs/pearl/pull/311) had not yet been merged. The existing public vLLM plugin and the FP8 mining implementation under development are separate milestones.

Even with FP8 inputs, differences in quantization scales, accumulation precision, or rounding points can change the result. In floating-point arithmetic, even `(a + b) + c` and `a + (b + c)` can differ. A small numerical difference can change transcript bits, which in turn can change the hash and whether an attempt wins.

On September 25, 2026, I directly compared matrix-multiplication results from Pearl's public FP8 simulator with results from my RTX 5090. Under the conditions I tested, I found no bit mismatches across up to 4,194,304 output values.

That establishes agreement for those tested conditions. It does not establish FP8 mining support or profitability on the RTX 5090. The actual mining kernel and protocol need to support it, and untested inputs and edge cases remain.

The [BF16 rounding edge-case issue](https://github.com/pearl-research-labs/pearl/issues/424) linked to the [FP8 implementation PR](https://github.com/pearl-research-labs/pearl/pull/311) shows why those edge cases matter. For the reported input, a small difference between the verifier's integer-based calculation and a CPU emulation of GPU arithmetic produced rounded RMS values of `1.0` and `1.03125`. Because that value affects the FP8 quantization scale, the same input could lead to different operands and mining records. The report is a CPU reproduction, not a result verified by running the actual CUDA implementation.

I found this rounding problem particularly interesting. A small error that inference can tolerate can become a problem for consensus rules used to verify computation across participants. Details like this help determine which hardware and services can support mining.

## What happens as competition grows?

Under the conditions in which I ran one RTX 5090, it mined about 6.5 PRL per day. At the price then, the rewards were worth several times the electricity bill. That was not net profit after hardware purchase and depreciation, and the calculation changes immediately with price and difficulty. Today's output is not enough to judge long-term profitability.

I expect operators with efficient hardware and real inference demand to gain an advantage as competition grows. Data-center GPUs such as the B200 may become favorable in more situations, but it would be too strong to say that only those devices will remain profitable as difficulty rises. Kernel support, throughput for each model, hardware prices, and electricity costs all matter.

What I picture is **AI server GPUs taking on an ASIC-like role in the PoUW era**. In Bitcoin, specialized ASICs became central to mining because they compute SHA-256 quickly and efficiently. In a matrix-multiplication-based PoUW system such as Pearl, GPUs optimized for AI could occupy a similar competitive position. The analogy is about their role in mining. The ability to perform AI's matrix multiplications efficiently would also become a source of mining competitiveness.

What makes this interesting is that the same hardware already has a market in inference and training. A server purchased for AI services could also mine through the same computation, while remaining useful for AI if rewards declined. [Pass's paper discusses GPUs' uses outside mining](https://arxiv.org/html/2606.06700v1#S1.SS8) as an important difference from ASICs. If this combination takes hold, I think competition in mining will overlap with competition to run AI infrastructure efficiently. Investments in AI chips and inference software could contribute to blockchain security as well as service performance.

None of this guarantees that mining rewards will keep reducing costs. Issuing tokens does not remove electricity or hardware bills, and there must be demand for those rewards. [Rafael Pass's paper on the economics of PoUW](https://arxiv.org/abs/2606.06700), released in June 2026, models competition among pure mining, pure inference, and doing both together. It analyzes how inference prices and supply change under different conditions. I read it as a framework for thinking about costs and demand, rather than as a prediction of token prices.

I find it plausible that participation from a large AI compute market could increase the computation available to secure a network. But the world's GPUs do not automatically secure this particular network. What matters is how much compute actually participates, how concentrated it is among operators, and how difficult it would be to rent or redirect outside GPUs into an attack. In Pass's model, the economic cost of a majority attack remains tied to the value of block rewards. Nor does the fact that GPUs have other uses immediately imply that attacks become cheap. [The paper's security analysis and limitations](https://arxiv.org/html/2606.06700v1#S1.SS8)

## I see PoUW as part of a larger shift

I believe PoUW will become a major new trend. I do not know whether Pearl will remain one of the projects leading it. But the idea of combining necessary AI computation with work that secures a network, and using the rewards to share the cost, could outlast the success or failure of any one project.

The longer I operate servers, the more the cost of serving a request matters alongside model quality. Small differences add up over many requests. If PoUW can lower that cost while preserving service quality and speed, even a small operator like me has a reason to consider it. Alongside current mining output, I am watching how easily it integrates with inference engines and how many real requests it can support.

We plan to apply Pearl's PoUW to the local inference traffic we already serve, with the aim of reducing costs. First, we will check what support the vLLM plugin needs for our models and RTX PRO 6000 Blackwell setup. I want to compare mining on and off with the same model, input lengths, batch settings, and precision, measuring response quality, tokens per second, time to first token (TTFT), inter-token latency, and power consumption. I also want to check whether proof generation causes unusually long delays for some requests. We have not run this service comparison yet.

We bought the server so that we would not depend entirely on external models. The services we need must keep running even if mining rewards fall. Within that constraint, I want to find out how much PoUW changes the cost of a real request. Next time, I hope to write about measurements from my own server.
