# Chapter V: MEV

*This section examines Maximal Extractable Value: who extracts it, how it impacts users and markets, and the design space for mitigation across ecosystems.*

## Section 1: The Complex World of MEV

**Maximal Extractable Value (MEV)** is the profit block producers can capture by strategically ordering, including, or excluding transactions within the blocks they create. This concept, originally called **"Miner Extractable Value"** during Ethereum's proof-of-work era, represents revenue extracted beyond standard block rewards and transaction fees. The process begins when users submit transactions to a public **"mempool,"** a waiting area where block producers can observe pending trades and leverage this advance knowledge for profit.

This has fostered a sophisticated ecosystem with distinct roles. **Searchers** scan the mempool for profitable opportunities, **builders** construct optimized blocks to capture this value, and **proposers** (validators) select the most profitable blocks to add to the chain. This relationship has been formalized by systems like **MEV-Boost**, which creates a liquid market for block space.

Imagine a busy market with a big whiteboard listing everyone's pending orders — that's the public **mempool** (whiteboard = mempool). A fast **searcher** (reseller) watches the board, sees you're about to buy 10 tomatoes from a **DEX/pool** (stall), sprints ahead, buys first, then offers them back to you at a markup — a **front-run**.

They also slip in a buy just before your order and a sell just after it, using your price impact to lock in a risk-free spread — a **sandwich**. Meanwhile the **block builder/validator** (market manager) starts auctioning the right to decide checkout order; whoever tips most goes first — aggressive **fee bidding** for ordering priority.

Some line-jumping (like backruns that align prices across stalls or liquidate bad debt) can stabilize the market, but regular shoppers end up paying more and waiting longer, while only well-funded pros with the fastest runners and private backrooms consistently win — increasing **centralization**.

So what is MEV? It's the value captured by controlling transaction visibility and ordering. It raises user costs and worsens execution unless mitigated by tools like private order flow, batch auctions, fair ordering, or builder/validator separation.

In this context, Ethereum is often called a "dark forest": revealing a profitable transaction in the public mempool can summon "generalized frontrunner" bots that copy, mutate, and preempt it before inclusion. The takeaway is that visibility itself is risk, which motivates private order flow, order‑flow auctions, and PBS-style designs to reduce exposure and return value to originators.

### Common MEV Strategies

- **Arbitrage**: Profiting from price differences for the same asset across different exchanges.
- **Liquidations**: Claiming rewards for closing undercollateralized positions in DeFi protocols.
- **Front-running**: Copying a profitable user transaction and paying a higher fee to have it executed first.
- **Sandwich Attacks**: Placing trades before and after a user's large trade to manipulate the price and extract value.

**Frequent batch auctions** and **intent-based settlement** (e.g., CoW Swap, Uniswap X) mitigate sandwiching by removing continuous-time priority.

### MEV's Centralizing Pressure and Proposed Solutions

While MEV activities like arbitrage can enhance market efficiency and liquidations are a necessary function, the overall impact presents a fundamental tension between market mechanics and user fairness. MEV competition inflates gas prices for all users as bots bid aggressively for transaction priority. Furthermore, users often receive worse execution prices from front-running and sandwich attacks, effectively paying an **"invisible tax"** to sophisticated actors.

This dynamic creates significant **centralization pressures**, as success requires substantial capital and technical expertise. On Ethereum, this has led to concentration among builders, with recent research showing **Titan was ~32% of blocks with TC interactions**, and **~19% of blocks were produced by sanction-enforcing producers** (as of 2024–2025; shares fluctuate by dataset and definitions, especially what counts as “sanction‑enforcing”).

To counter this, a decentralized block-building network called **BuilderNet** was announced in 2024 by Flashbots, Beaverbuild, and Nethermind (as of 2025‑05). BuilderNet uses **Trusted Execution Environments (TEEs)** to allow multiple operators to share transaction order flow and coordinate block building while keeping the contents private until finalized. This architecture aims to create a more transparent and permissionless system for MEV distribution, moving away from the opaque, custom deals that define the current landscape. Beaverbuild is already in the process of transitioning its centralized builder to this new network, with more permissionless features planned for future releases.

**Order flow auctions (OFAs)** and **private orderflow** (e.g., MEV-Share, SUAVE, private relays, encrypted mempools, private RPCs) seek to return value to users—often via rebates—with mixed results in practice. **Time-bandit attacks** (reorgs to capture MEV) are constrained by fast finality; research explores **MEV-smoothing** and **enshrined PBS**.

### Emerging Challenges: Cross-Domain MEV

A new frontier of value extraction, **Cross-Domain MEV**, is also emerging. This refers to arbitrage and other strategies executed across different blockchain networks, exploiting price differences between on-chain exchanges on separate chains. Researchers warn this could pose an **"existential risk"** to decentralization if sophisticated actors gain control over transaction ordering across multiple domains. The timing and latency of blockchain bridges are critical factors, enabling complex, multi-block MEV strategies that are even harder to mitigate. This highlights that as the blockchain ecosystem grows, the challenges of ensuring fair and decentralized value extraction will only become more complex. See also: Chapter II, Section 3 for PBS on Ethereum and rollup builder dynamics.

Mitigations under study include **shared sequencing** across domains, **cross-domain batch auctions**, and **routing intents through OFAs**.

## Key Takeaways
- **MEV arises from transaction ordering**; roles split into searchers, builders, proposers via PBS/MEV-Boost.
- **Harmful MEV** (e.g., sandwiching) increases user costs; mitigations include batch auctions, intents, OFAs, and private orderflow/private RPCs.
- **Centralization pressures** in block building spurred designs like BuilderNet and research into enshrined PBS.
- **Cross-domain MEV** is growing; shared sequencing and cross-chain auctions are active mitigation areas.