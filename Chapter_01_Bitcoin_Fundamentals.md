# Chapter I: Bitcoin Fundamentals

## Section I: Bitcoin Core Concepts

### Genesis and Philosophy

Bitcoin's creation was a direct response to the 2008 global financial crisis. On January 3rd, 2009, its anonymous creator, Satoshi Nakamoto, embedded a newspaper headline into the very first block, known as the genesis block. The headline—*The Times*, "Chancellor on brink of second bailout for banks"—serves as a permanent critique of a traditional financial system dependent on centralized control.

This act highlights Bitcoin's mission: to be an alternative to the traditional banking system. Its philosophy is rooted in the cypherpunk belief in using strong cryptography to achieve individual sovereignty over one's finances. To accomplish this, Bitcoin operates as a peer-to-peer electronic cash system without trusted third parties. Its monetary policy is predictable and enforced by code, featuring a fixed, immutable supply cap of 21 million BTC. This creates digital scarcity, standing in stark contrast to fiat currencies that central banks can print at will.

But creating a decentralized alternative to traditional banking raises a fundamental challenge: how do you get thousands of computers around the world to agree on who owns what, without a central authority to settle disputes? This is where Bitcoin's consensus mechanism becomes crucial.

### Consensus and Chain Selection

When there's no central bank or clearinghouse, the network itself must agree on the true history of transactions. Bitcoin solves this through a robust consensus mechanism. Bitcoin uses **Nakamoto Consensus**, which is often simplified as the "longest chain rule" but is more accurately described as the "heaviest chain rule." The canonical chain is the one with the most accumulated computational work invested in it, not necessarily the one with the most blocks.

Think of finding a block as a lottery; chainwork is the total sum of "lottery tickets" (hashes) required to build the entire chain, a value calculated from the difficulty target (nBits) of each block. A shorter chain could have a higher cumulative difficulty, making it the valid one. This prevents an attacker from overwriting history with a long but easy-to-produce chain, as the sheer energy invested in the honest chain makes it prohibitively expensive to overcome.

Imagine two climbers racing to the summit on different routes. One takes 1,000 easy steps up a gentle trail; the other takes 600 steps up a steep face where each step is worth more points because it’s harder. The judges don’t count steps; they total points. That’s chainwork: nodes sum per‑block work (from each block’s nBits) and choose the chain with the most total work—even if it has fewer blocks.

### Mining and Proof-of-Work

What if you needed to prove you'd done a lot of work, but couldn't trust anyone to verify it? Bitcoin solves this through **Proof-of-Work**—a system where miners compete to solve cryptographic puzzles that require enormous computational effort but can be instantly verified by anyone.

Here's how it works: Miners bundle transactions into a block and repeatedly hash the block header using the double SHA-256 algorithm. They're searching for a hash value below a specific target—like rolling dice until you get a number lower than a certain threshold, except they're "rolling" trillions of times per second.

To do this, miners primarily vary a field in the header called the **nonce**, a 32-bit number offering about 4 billion guesses. When those are exhausted, miners can alter the **extranonce** within the coinbase transaction, which changes the block's Merkle root and provides a new range of hashes to test. To keep the average block time at approximately 10 minutes, the network performs a **difficulty retarget** every 2,016 blocks (about two weeks). If blocks are found too quickly, the difficulty increases; if too slowly, it decreases.

Most hashpower is coordinated through mining pools using specialized ASIC hardware. Pools distribute work via the **Stratum protocol** (v2 improves security and job negotiation). Stale blocks and short-lived chain reorganizations are normal; confidence increases with confirmation depth.

### Monetary Policy

Bitcoin has a predictable, algorithmic monetary policy with a fixed issuance schedule. The **block reward**, or subsidy, is cut in half every 210,000 blocks, an event known as the **"halving"** that occurs roughly every four years. The subsidy began at 50 BTC and has since been reduced to 25, 12.5, 6.25, and most recently to 3.125 BTC after the 2024 halving.

This mechanism makes Bitcoin a **disinflationary asset**, as its inflation rate trends toward zero. Around the year 2140, the subsidy will cease, and miners will be compensated solely by transaction fees. This predictable scarcity is a cornerstone of Bitcoin's value proposition as a store of value, though scarcity alone doesn't guarantee price appreciation—that requires sustained demand to accompany the diminishing supply.

Due to integer rounding in halvings, the terminal supply converges to ~20,999,999.9769 BTC. Over time, miner security budgets shift from subsidy to fees, making a healthy fee market important for long-term incentives.

---

## Section II: Bitcoin Technical Architecture

### UTXO Model

How do you track ownership in a system without accounts? Bitcoin takes a radically different approach from traditional banking by using an **Unspent Transaction Output (UTXO) model**.

Think of it like physical cash in your wallet. Instead of having a single account balance, you have individual bills of different denominations—a $20, two $5s, and some $1s. When you buy something for $7, you might use a $5 and two $1s, getting back change if needed.

Bitcoin works similarly. Instead of a single balance, your wallet holds a collection of UTXOs—individual digital "coins" of varying amounts. When you send bitcoin, your wallet selects UTXOs as inputs, consumes them entirely, and creates new UTXOs as outputs: one for the recipient and another as "change" back to you.

This model enhances privacy by encouraging the use of new addresses for change outputs and offers potential scalability benefits by allowing parallel transaction processing. Full nodes are responsible for tracking the entire network's **UTXO set**, which is the complete collection of all spendable outputs available for future transactions.

**Bitcoin Script** is a simple programming language that locks and unlocks UTXOs using different address types. **Timelocks** allow transactions to be delayed until a specific time or block height, enabling more complex contracts like Lightning channels, vaults, and escrow arrangements.

### Transaction Structure and Prioritization

Once you understand how UTXOs work, the next question is: how do transactions actually get processed? A Bitcoin transaction consists of **inputs** (the UTXOs being spent) and **outputs** (the new UTXOs being created). Once broadcast, transactions enter the **mempool**—think of it as a waiting room for unconfirmed transactions.

Here's where economics comes into play. Since each block has limited space, miners must choose which transactions to include. They naturally prioritize transactions that pay the highest **fee rate**, measured in satoshis per virtual byte (sats/vB). A satoshi is the smallest unit of bitcoin—there are 100 million satoshis in one bitcoin.

This creates a **fee market** where users essentially bid for block space. Need your transaction confirmed quickly during network congestion? Pay a higher fee rate. Can wait? Pay less and wait for a quieter period.

Users can also use **Child-Pays-for-Parent (CPFP)** to boost stuck transactions by creating a new transaction that spends from the unconfirmed one with a higher fee rate, incentivizing miners to include both.

### Address Types and Formats

Bitcoin addresses have evolved to improve efficiency and enable new features. The primary types include:

Legacy — starts with 1
Oldest format. Works everywhere, but usually slightly higher fees.

P2SH — starts with 3
Compatibility format. Often used for multisig or older SegWit-in-a-wrapper. Works almost everywhere.
Myth-buster: 3... ≠ always multisig.

Native SegWit — starts with bc1q
Modern default for most wallets. Lower fees, safer to copy (all lowercase).

Taproot — starts with bc1p
Newest format. Enables advanced features and good fee efficiency. Supported by most modern wallets; a few services may still be catching up.

Wallets standardize address derivation using BIP32/39/44 and output descriptors; avoid address reuse to protect privacy.

---

## Section III: Bitcoin Upgrades and Scaling

### Segregated Witness (SegWit)

Activated in 2017, **Segregated Witness (SegWit)** was a landmark upgrade that solved a critical problem while paving the way for future innovations.

**The Problem: Transaction Malleability**
Before SegWit, Bitcoin had a critical bug: third parties could alter a transaction's signature and change its ID (TXID) before confirmation, without affecting the transaction's validity. This **transaction malleability** made it risky to build dependent transactions or second-layer protocols.

**The Solution: Separating Witness Data**
SegWit solved this by removing the witness (signature) data from the part of the transaction used to calculate the TXID. The signatures were moved to a separate structure, making transaction IDs immutable once created.

**The Bonus: Increased Capacity**
This architectural change also introduced **block weight**, a new way of measuring transaction size. Instead of a simple 1MB limit, Bitcoin now uses a 4,000,000 weight unit maximum. This effectively increased block capacity while incentivizing users to adopt the more efficient SegWit addresses.

The weight system gives witness data a 75% discount compared to other transaction data. Fees are commonly quoted in **virtual bytes (vB)**, which account for this discount and provide a simpler way to calculate transaction costs.

### Soft Forks

How do you upgrade a decentralized network where no one's in charge? Bitcoin uses **soft forks**—backward-compatible protocol upgrades that tighten consensus rules without breaking the network.

Think of it like adding a new traffic law. If the speed limit changes from 65 mph to 55 mph, older cars that don't know about the change can still drive on the road—they just might unknowingly break the new rule. Similarly, non-upgraded Bitcoin nodes still see new blocks as valid; they simply don't enforce the stricter rules themselves. This allows the network to upgrade without splitting into incompatible versions.

An early example was disabling the OP_CAT opcode in 2010 to prevent potential denial-of-service attacks. More recent upgrades like SegWit and Taproot followed this same pattern.

**The Challenge of Change**
Despite backward compatibility, getting any soft fork into Bitcoin is intentionally difficult. Many developers prioritize simplicity and **protocol ossification**—the idea that Bitcoin should become increasingly resistant to change as it matures. They view even small modifications as sources of uncertainty and risk.

This conservative approach means proposals undergo years of review, testing, and community debate. Nearly every soft fork discussion—including SegWit, Taproot, and newer proposals—generates controversy over activation methods, safety assumptions, and long-term precedent.

### Replace-by-Fee and Standards

**Replace-by-Fee (RBF)** is a feature that allows users to increase the fee on an unconfirmed transaction. Defined in BIP-125, **opt-in RBF** lets a sender mark a transaction as replaceable, giving them the option to rebroadcast it with a higher fee to ensure faster confirmation during network congestion. Since Core v24, nodes can optionally enable **full-RBF** via the `mempoolfullrbf` flag; replacement behavior can therefore differ by peer and pool.
Another network feature is the **OP_RETURN opcode**, which allows users to embed a small amount of arbitrary data in a transaction. In 2025, Bitcoin Core v30's default policy removes the historical 80-byte relay cap; from v30 onward, default policy allows OP_RETURN outputs up to nearly 4 MB. Earlier Core releases retain their prior defaults, and peers/miners can set tighter limits. These are relay/policy settings, not consensus, and behavior can vary by node version and operator policy over time.

### Taproot and Advanced Features

The **Taproot upgrade**, activated in 2021, significantly improved privacy, efficiency, and smart contract capabilities. It combines two key technologies:

1. **Schnorr Signatures**: These allow for key and signature aggregation through schemes like MuSig2, enabling complex multi-party transactions to be represented by a single signature on-chain.

2. **Merkleized Abstract Syntax Trees (MAST)**: This allows complex spending conditions to be structured in a way that only the condition that is met needs to be revealed.

Together, these features make complex transactions indistinguishable from simple payments for key-path spends, providing a major boost to privacy and scalability; when a script-path branch is used, only the revealed branch is disclosed.
Taproot supports both simple single-signature payments and complex script-based conditions. Key-path spends are indistinguishable from simple payments; script-path spends reveal the used branch.

---

## Section IV: Bitcoin Layer 2 and Extensions

### Lightning Network

What if you could make instant Bitcoin payments without waiting for block confirmations or paying high fees? The **Lightning Network** makes this possible through a clever Layer 2 protocol that moves most transactions off the main blockchain.

The concept is elegantly simple: instead of broadcasting every payment to the entire network, two parties can open a private **payment channel** by locking funds in a shared on-chain account (technically a 2-of-2 multisig output).

Once the channel is established, the parties can transact an unlimited number of times by updating their channel's balance sheet off-chain. All state changes require mutual agreement and are secured by cryptography. When they are finished, they can close the channel by broadcasting the final state to the Bitcoin blockchain. The network can also route payments across multiple interconnected channels.

Lightning uses **HTLCs** and **onion routing** for private, trust-minimized payments; **watchtowers** help penalize cheating. Channel liquidity is directional (inbound vs outbound) and affects routing success; rebalancing and swap services help manage liquidity for reliable routing.

Think of Lightning as a canal system with locks. You can only send a boat if there’s enough water on your side (outbound capacity), and you can only receive if the other side has room to raise water to meet you (inbound capacity). Multi-hop routes work only when each lock along the path has water oriented the right way. Rebalancing is like shifting barges to move water back without closing the canal. HTLCs are sealed containers that either pass every lock intact or return unopened; onion routing means each lock‑keeper sees only the next hop, not the whole voyage.

---

## Section V: Bitcoin Network Operations and Security Model

### Roles at a Glance

**Users/wallets** create and sign transactions, then broadcast them to the network (you can do this without running your own node). **Full nodes** independently validate and relay transactions and blocks, enforcing consensus rules for themselves (running a node is not the same as mining). **Miners** assemble validated transactions into candidate blocks and perform Proof‑of‑Work to win block production (miners typically run a full node, but mining is the energy‑intensive block creation role).

### Node Types and Network Topology

The Bitcoin network is a decentralized system composed of different participants:

- **Full nodes** form the network's backbone, storing the complete blockchain and independently validating all transactions and blocks against consensus rules.
- **Pruned nodes** offer the same validation security but discard old block data to save disk space.
- **SPV (Simplified Payment Verification) clients**, common in mobile wallets, download only block headers and trust full nodes for transaction validation.

To maintain its decentralized topology, the network relies on **DNS seeds** and peer-to-peer exchange for discovering other nodes.

### Block Propagation and Network Synchronization

When a new node joins, it performs an **Initial Block Download (IBD)** to sync the entire blockchain from its peers. To ensure new blocks propagate quickly and efficiently, the network uses optimized protocols like **Compact Block Relay**, which minimizes bandwidth by only sending information that nodes don't already have. Nodes also engage in **mempool synchronization** to share unconfirmed transactions. The network is resilient to partitions (temporary splits), which self-heal once connectivity is restored.

Additional efforts like **FIBRE** (fast relay) and **Erlay** (proposed mempool gossip reduction) improve propagation latency and bandwidth efficiency.

### Attack Vectors and Economic Security

Bitcoin's security is economic and probabilistic. The most cited threat is a **51% attack**, where an entity controlling a majority of the network's hashpower could attempt to rewrite history. However, the immense cost of acquiring and running this hardware, combined with the fact that a successful attack would devalue the asset, makes it economically irrational.

Security is achieved through **confirmation depth**; each subsequent block exponentially increases the work required to alter a transaction. This leads to **probabilistic finality**, where after a certain number of confirmations (e.g., six), a transaction is considered irreversible. The system is designed so that economic incentives strongly reward miners for honest behavior.

Other threats include **eclipse attacks** (peer isolation) and **selfish mining**; diversity of peers, network-level protections, and monitoring help mitigate these risks.

### Key Management and Wallet Security

The foundational principle of self-custody is **"Not your keys, not your coins."** Securely managing private keys is paramount:

- **Hierarchical Deterministic (HD) wallets** generate a nearly infinite number of addresses from a single backup seed phrase.
- **Multi-signature wallets** require multiple keys to authorize a transaction, distributing trust and securing funds.
- **Hardware wallets** provide the highest level of security by keeping private keys completely offline, isolated from internet-connected devices.

### Privacy Model and Chain Analysis

Bitcoin is **pseudonymous**, not anonymous. While addresses are not directly linked to real-world identities, transaction graph analysis can be used to cluster addresses and track the flow of funds. This risk is significantly increased by address reuse. Furthermore, **KYC/AML** (Know Your Customer/Anti-Money Laundering) regulations at exchanges create links between on-chain activity and real-world identities, creating privacy gaps.

Common privacy practices include avoiding address reuse, using coin control, and optionally leveraging **CoinJoin-style tools** to reduce heuristic linking.

### Network Economics and Fee Markets

As we discussed in the transaction prioritization section, Bitcoin's limited block space creates a competitive fee market. This economic dynamic becomes increasingly important over time, as fee revenue must eventually replace the diminishing block subsidy as the primary incentive for miners.

At a system level, the miner **security budget** is total revenue paid to block producers over time: subsidy + fees (per block, per day, or per epoch). Expressed in BTC this is straightforward, but for gauging attack resistance the relevant unit is typically **USD per unit time**, since both miners and potential attackers procure hardware, facilities, and energy in fiat terms. As specialized hardware improves, the cost per hash declines; holding "hashes" constant does not hold attacker cost constant. What matters economically is the dollar cost to acquire and operate enough hashpower for long enough to reliably reorganize the chain.

This framing underscores a long‑run concern: the subsidy halves roughly every four years (see Monetary Policy above). If transaction fees and/or BTC price do not rise sufficiently to offset successive halvings, the USD‑denominated security budget trends lower. A materially smaller budget can lead to miner exits, weaker competition for blocks, and a lower dollar cost for would‑be attackers to rent or acquire a majority share of hashrate for a window of time. In the limit (around 2140) the subsidy falls to ~0, so durable **fee demand** must carry the full security budget—via payments, L2 settlements, inscriptions, batched rollup data, and other valuable uses of block space. Healthy fee markets over the cycle are therefore not a cosmetic metric; they are the funding mechanism for Bitcoin’s long‑term security.

### Network Resilience and Antifragility

Bitcoin is designed to be **antifragile**—it grows stronger from stress and attacks. Its resilience stems from several factors:

- Geographic distribution of nodes and miners resists localized disruptions.
- **Protocol ossification**, or resistance to change, enhances stability and predictability.
- Its design assumes an adversarial environment, built to function despite malicious actors.

The network has survived numerous technical, political, and economic challenges, demonstrating its robust and self-healing nature.

### Bitcoin Inscriptions and Ordinals

**Ordinal Theory** is a social convention that assigns a unique serial number to every satoshi, allowing individual sats to be tracked and transferred. **Inscriptions** use this method to embed arbitrary data, like images or text, into the witness portion of a Bitcoin transaction.

This process became practical thanks to two soft forks: SegWit, which provided a block space discount for witness data, and Taproot, which enabled more flexible and larger script paths.

**BRC-20 tokens** are an experimental standard built on this technology, using JSON text inscriptions to signal "deploy," "mint," and "transfer" functions. An important limitation is that BRC-20s have no native token logic in consensus. Their state is not enforced by the Bitcoin protocol itself but is tracked by off-chain indexers that interpret the inscribed data.

Relay and mining policies for large inscriptions can vary, affecting inclusion and propagation.

## Section VI: Bitcoin in Practice - Corporate Adoption

How do Bitcoin's fundamental properties translate into real-world adoption? One of the most visible examples has been corporate treasuries adding Bitcoin to their balance sheets.

### The Corporate Treasury Trend

Beginning in 2020, a handful of public companies began allocating portions of their corporate cash reserves to Bitcoin. They viewed it as a long-duration, non-sovereign monetary asset that could serve multiple purposes: portfolio diversification, inflation hedging, and brand alignment with digital-native finance.

This trend reflects Bitcoin's evolution from a niche digital experiment to an asset class that major corporations consider suitable for treasury management, though adoption remains limited relative to total corporate cash balances.

### The Strategy Playbook

**Strategy** (formerly known as MicroStrategy; rebranded Feb 2025, ticker MSTR) developed a financing playbook to accumulate Bitcoin at scale. The approach centers on issuing **senior unsecured convertible notes** at low coupons—including $2B of 0% due 2030—alongside at‑the‑market (ATM) equity programs.

The key dynamic is that MSTR's stock volatility (variable; often markedly higher than broad equity indices) makes the embedded **conversion option** valuable to institutional investors. Convert‑arb funds buy the bonds and hedge the equity, monetizing volatility via **gamma trading**.

This creates a self-reinforcing cycle: bond proceeds fund Bitcoin purchases → Bitcoin holdings increase net asset value → stock price rises → higher volatility makes future convertible issuances even cheaper → cycle repeats.

### Performance and Risk Profile

The strategy has delivered notable results while maintaining structural protections against liquidation. Strategy reported ~**74% BTC Yield** for FY2024 (their KPI measuring % change in BTC per share) and holds ~**636,505 BTC**. At BTC $110,000, that stack is ≈ **≈$70B**.

- **Liquidation risk remains minimal** due to several factors:
- Convertible notes are **senior unsecured** with no BTC collateral requirements
- Outstanding maturities are 2028, 2030 (two tranches), 2031, and 2032; the 2027 notes were settled earlier in 2025 via conversion/redemption (the company received conversion requests for substantially all of the $1.05B before the Feb 24, 2025 redemption date)
- Conversion prices vary by tranche; being "in the money" depends on the strike:
  - 2028 notes: ~$183.19/share (ITM above that)
  - 2030 0% notes (issued Feb 2025): ~$433.43/share
  - 2032 notes (Jun 2024): ~$2,043.32/share
  - 2031 notes: >$2,300/share
- Cash interest outlay depends on the mix of 0% converts (no coupon) and preferred dividends (e.g., STRK/STRF at ~8–10%). SEC filings indicated materially higher annualized interest on remaining notes prior to the 2030 0% issuance; given changes over time, avoid a point estimate without a dated source.
- Authorized capacity includes a disclosed **$21B common‑stock ATM** and a separate **$21B preferred (STRK) ATM**

### Strategic Risks and Limitations

The flywheel mechanism faces several critical vulnerabilities:

**Premium compression** represents the primary threat—if MicroStrategy's stock price converges toward its Bitcoin net asset value, the effectiveness of their accretive dilution strategy diminishes significantly.

The model exhibits **diminishing returns at scale**: the company required just 2.6 Bitcoin to generate one basis point of yield in 2021 but needed 58 Bitcoin by 2025 for the same result.

Long-term success depends on three key conditions: Bitcoin maintaining its upward trajectory, MicroStrategy's stock preserving high volatility to attract convertible arbitrageurs, and continued access to capital markets for refinancing operations. While these conditions persist, the company appears positioned to continue its Bitcoin accumulation strategy with structural protections against forced liquidation.

---

## Key Takeaways
- Bitcoin targets self-sovereign money with a fixed 21M cap and disinflationary issuance via halvings.
- Consensus follows the heaviest-work chain; PoW security relies on economic cost and confirmation depth.
- The UTXO model, Script, and timelocks enable simple contracts; fee markets prioritize by sats/vB.
- SegWit fixed malleability and introduced block weight; Taproot (Schnorr + MAST) boosts privacy/efficiency.
- Lightning enables instant, low-fee payments through off-chain channels secured by on-chain enforcement.
- Security is probabilistic; threats include 51% and eclipse attacks, mitigated by decentralization and incentives.
- Address evolution (P2PKH → SegWit → Taproot) improves efficiency; avoid reuse to preserve privacy.
- Fees will increasingly replace subsidy; a healthy fee market is critical for long-term miner incentives.
- Ordinals/inscriptions use witness space; BRC-20s are indexer-defined, not enforced by consensus.