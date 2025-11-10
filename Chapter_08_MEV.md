# Chapter VIII: MEV

Control over transaction ordering creates and redistributes value on-chain. This chapter connects market microstructure to MEV: who extracts it, how it impacts users, and what mitigations (private order flow, batch auctions, proposer-builder separation) can return value or reduce harm.

## Section I: The Market Chaos: Understanding MEV Fundamentals

Picture a busy marketplace with a peculiar setup. A big whiteboard where everyone must post their intended purchases before they can buy anything. A trader writes "buying 10 tomatoes from Stall A," and suddenly chaos erupts.

A fast-moving reseller spots the order, sprints to Stall A, buys the tomatoes first, then offers them back to the trader at a markup. Another reseller notices the trader is about to make a large purchase that will drive up tomato prices, so they buy just before the trader and sell immediately after, pocketing the price difference the trade created. Meanwhile, the market manager starts auctioning off the right to decide who gets served first: whoever pays the highest tip jumps to the front of the line.

This market chaos isn't just an analogy but exactly what happens in **the public mempool**, creating what researchers call a "dark forest" where revealing profitable trades attracts predators.

**Maximal Extractable Value (MEV)** is the profit that emerges from this system. Originally called "Miner Extractable Value" during Ethereum's proof-of-work era, MEV represents revenue extracted beyond standard block rewards and transaction fees by strategically ordering, including, or excluding transactions within blocks.

In our market analogy, the key players have clear roles: **searchers** are the fast-moving resellers scanning for opportunities, **builders** are market managers who construct blocks and bid their value to **proposers** (validators), and **proposers** are the market owners who choose which manager's arrangement to accept. This relationship has been formalized through auction systems that create a liquid market for block space by essentially letting market managers bid for the right to organize transactions.

The fundamental insight is that MEV arises from controlling transaction visibility and ordering. Some activities, like ensuring prices stay aligned or liquidating bad debt, can stabilize the market. However, the overall effect imposes an implicit tax on regular users through worse execution, while only well-funded professionals with the fastest infrastructure consistently win.

This creates the core tension: how transaction ordering, designed to be neutral infrastructure, becomes a sophisticated value extraction mechanism that threatens the very decentralization it's meant to serve.

## Section II: How Value Gets Extracted

### Benevolent vs. Malignant MEV

Before examining specific extraction strategies, we need a framework for evaluating their market impact. Not all MEV harms markets equally, and distinguishing productive from predatory extraction matters for both protocol design and user protection.

**Benevolent MEV** serves necessary economic functions. CEX-DEX arbitrage enforces price consistency across markets, preventing exploitable price divergences that would otherwise destabilize trading. Liquidations preserve the solvency of lending protocols by ensuring under-collateralized positions get closed before they become bad debt that would burden all protocol users. These activities extract value, but they also deliver clear benefits: tighter price spreads and healthier lending markets.

**Malignant MEV** extracts value without providing commensurate benefits. Sandwich attacks exemplify this: the victim pays more, the searcher profits, and the market gains nothing. This is pure wealth transfer enabled by privileged information and ordering control.

Between these extremes sit context-dependent behaviors that blur the line. JIT (Just-In-Time) liquidity on Uniswap v3 demonstrates this ambiguity: searchers deposit concentrated liquidity milliseconds before a large trade, capture the fees, then immediately withdraw. On one hand, this provides liquidity exactly when needed and can reduce slippage for the trader. On the other hand, it crowds out passive liquidity providers who can't compete with such precision, potentially degrading liquidity depth over time.

Similarly, back-running oracle updates can stabilize prices by immediately arbitraging stale rates after fresh data arrives, but this speed advantage means specialized operators capture value that might otherwise accrue to regular arbitrageurs or traders. The system benefits from rapid price corrections, yet the concentration of profits among those with the fastest infrastructure raises fairness concerns.

The key distinction isn't whether value gets extracted (it always does), but whether that extraction serves a necessary function or merely exploits information and ordering advantages. This framework helps us evaluate the strategies that follow.

### MEV Extraction Strategies

From this chaos emerged a hierarchy of exploitation strategies, each more sophisticated than the last. The simplest is **arbitrage**: buying an asset at a lower price on one exchange to sell it at a higher price on another. This benevolent form of MEV actually helps the market by keeping prices aligned across different venues, but when competition heats up, searchers get more aggressive.

They start **front-running**, copying a trader's transaction but paying extra to go first. For example, when a trader spots an arbitrage opportunity where they can buy ETH for $3,000 on one DEX and immediately sell it for $3,050 on another DEX, a bot sees the transaction and submits the exact same arbitrage trade with higher gas fees to capture that $50 profit before the trader can.

Then comes the most predatory strategy: the **sandwich attack**. Understanding why these work requires understanding AMM mechanics. Uniswap's deterministic pricing curve and public mempool visibility create predictable price impact. AMMs must move price with each swap (that's how they discover fair value without order books), transaction intent is visible and reorderable in the mempool, and off-chain markets provide price anchors for profitable extraction.

Consider a representative sandwich attack. A trader submits a transaction to swap ETH for USDC on Uniswap. A searcher's bot detects this pending transaction in the mempool and immediately constructs a three-transaction bundle:

1. **Front-run**: The bot buys USDC using ETH, pushing the pool price higher.

2. **Victim's trade executes**: The trader's swap now executes at the inflated price, receiving significantly less USDC than expected based on the original pool state.

3. **Back-run**: The bot immediately sells its USDC position back to the pool. As the price settles back down, the bot exits with a profit after accounting for gas fees and slippage.

The trader pays an invisible tax for revealing their intent publicly. The bot risks minimal capital (the trade bundle either executes atomically or reverts entirely) while extracting pure profit. This single transaction illustrates the MEV extraction dynamic in miniature: sophisticated actors use privileged information about pending transactions to extract value from regular users through strategic positioning and timing.

**Beyond price manipulation, liquidations** represent another MEV category: when someone's borrowed too much against their collateral, searchers race to claim the reward for closing out the position. Unlike sandwiching, liquidations serve a necessary function, but this competition still inflates costs for everyone.

Priority-gas-auction bidding historically spiked gas costs as bots competed for transaction priority; today much of that competition is off-chain via specialized auction systems where searchers bid for transaction ordering rights, reducing broad mempool fee spikes but often shifting costs into worse execution for users or rebates captured by intermediaries. This isn't just theoretical harm. Every sandwich attack represents value directly transferred from a user to a well-capitalized operator, even if the fee externalities now appear less in the public mempool and more in private routing markets.

### How Users Can Protect Themselves

Given the MEV extraction landscape described above, what practical steps can users take? When submitting transactions to public mempools, assume exploitation is likely. Here are the primary defenses:

**Set Tight Slippage Tolerances:** Control how much worse a price you'll accept. Start with 0.5-1%, though tokens with low liquidity may still be vulnerable. Too tight (below 0.3%) risks failed transactions during normal swings. On public mempools, you pay gas even when transactions fail; private RPCs can avoid these costs.

**Use Private Orderflow Services:** Services like Flashbots Protect send transactions through private channels rather than broadcasting publicly. This protects against front-running and sandwich attacks. Benefits: failed transactions don't cost gas, and you may receive MEV savings refunds. Tradeoff: you must trust these services to route properly.

**Trade Through Batch Auction Systems:** CoW Swap groups orders and executes them simultaneously, preventing sandwich attacks (which rely on sequential processing). UniswapX uses Dutch-auction execution where parties compete to fill orders. Both approaches protect through mechanism design rather than just hiding intent.

**Split Large Trades:** TWAP (Time-Weighted Average Price) orders break trades into smaller pieces across multiple blocks, reducing per-trade price impact and making sandwich attacks less profitable. Combine with private RPCs or intent-based systems when possible.

**Choose MEV-Aware Venues:** Some platforms build protection into their design: batch auction venues (CoW Protocol, Gnosis Auction), encrypted mempools (Shutter Network, SUAVE/ePBS research), and Uniswap v4 pools with custom MEV protections like dynamic fees.

The goal isn't complete MEV elimination (impossible) but making extraction harder and less profitable. These protections help against sandwich attacks but don't stop all MEV types. The battle constantly evolves with new attack methods emerging regularly.

### A Warning About "Easy Money"

Observing the profitability of MEV extraction, some newcomers wonder whether they should become searchers themselves. A reality check: "being the searcher" isn't free money. Winning priority requires paying tips/fees and accepting price impact; mis-set slippage turns many attempts negative-EV. On AMMs, the bonding curve means each marginal unit gets pricier, so naive bots often donate value to professional searchers, builders, and validators when they mis-price priority or slippage. Without precise simulation and risk controls, frontrunning or sandwich attempts frequently overpay for execution and become self-taxing rather than extracting value.

## Section III: Flashbots: Taming the Dark Forest

These user-facing protections emerged partly because the industry recognized that individual defenses alone weren't enough. By 2020, Ethereum faced exactly this market chaos at scale. The priority gas auctions described earlier were creating network congestion, while miners were capturing MEV through opaque, off-chain deals that favored well-capitalized participants.

Enter **Flashbots**, a research organization founded in 2020 with a radical proposition: instead of trying to eliminate MEV, create transparent infrastructure to make it more fair and efficient. Their insight was that the current system was wasteful, and that channeling extraction through better infrastructure could reduce harm.

### MEV-Geth and the First Solution

In January 2021, Flashbots released **MEV-Geth** (a modified Ethereum client) with **mev-relay**, creating a private communication channel between searchers and miners. Instead of competing in the public mempool with escalating gas bids, searchers could submit transaction bundles directly to miners through this sealed-bid auction system. This moved the competition off-chain, reducing PGA spam in the public mempool while professional searchers could still compete for MEV opportunities.

### The Transition to Proof-of-Stake

When Ethereum moved to proof-of-stake in September 2022, the entire MEV landscape needed rebuilding. Flashbots developed **MEV-Boost**, an open-source middleware that provides **out-of-protocol Proposer-Builder Separation (PBS)**. This expanded the builder-validator relationship introduced earlier into a full competitive marketplace via **relays**. As of mid-2025, approximately 90% of Ethereum blocks are built via MEV-Boost.

**Important distinction:** This out-of-protocol PBS is separate from **enshrined PBS**, which would build these mechanisms directly into Ethereum's protocol rather than relying on external middleware. Enshrined PBS remains in development and research phases.

### How MEV-Boost Works

This process is facilitated by trusted entities called relays. Relays act as a neutral escrow and auctioneer: builders send them full blocks, and the relay verifies their validity and bid. The relay then forwards only the block header and the bid to the proposer (validators are also called proposers in this context). The proposer chooses a header without seeing the block's contents, preventing them from stealing the MEV opportunity. The system evolved from individual miners making direct deals to a sophisticated auction where multiple builders compete for validator selection, with relays facilitating the bidding process.

### Expanding User Protection

Recognizing that infrastructure alone wasn't enough, Flashbots launched Flashbots Protect, a service that routes user transactions through private mempools. This shields regular users from sandwich and frontrunning attacks while potentially providing rebates from captured MEV. The service works by bypassing the public mempool. These transactions still compete in the builder auction but are not exposed to public mempool predation.

The Flashbots approach represents a pragmatic philosophy: given that extraction is baked into how ordering markets function, the goal should be making it transparent, efficient, and less harmful. Rather than fighting the economic forces, they built infrastructure to channel them constructively. However, this infrastructure-based solution revealed an uncomfortable truth: organizing MEV markets efficiently also created powerful chokepoints that concentrated control in unexpected ways.

## Section IV: The Centralization Crisis

Despite Flashbots' innovations, the MEV ecosystem faces a fundamental challenge: concentration of power among a small number of operators.

The extent of this concentration becomes clear when examining recent data. In October 2024, just two builders produced 90% of blocks over a two-week period. From October 2023 through March 2024, three builders controlled approximately 80% of MEV-Boost blocks. During this same timeframe, a significant share of blocks, often around 60%, were relayed via OFAC-compliant infrastructure (adhering to U.S. Office of Foreign Assets Control sanctions). The pattern is unmistakable: these high barriers to entry have consolidated power among a handful of operators, directly undermining blockchain's decentralized principles.

The relay layer introduces additional centralization concerns. Because only a handful of trusted relays dominate the market, their compliance decisions (such as filtering transactions to adhere to OFAC sanctions) can have network-wide effects. These supposedly neutral intermediaries become powerful chokepoints that shape which transactions actually make it into blocks regardless of individual validator preferences. The choice of which relays to trust can determine transaction inclusion, making censorship resistance vulnerable to a small set of gatekeepers.

### Responses to Centralization

The concentration revealed by these metrics made clear that MEV-Boost alone couldn't solve the centralization problem. The relay layer remained a chokepoint, and builder concentration continued unabated. The industry needed more fundamental restructuring.

In November 2024, major players launched **BuilderNet**, a decentralized block-building network jointly operated by Flashbots, Beaverbuild, and Nethermind. BuilderNet uses **Trusted Execution Environments (TEEs)** to enable a novel approach: multiple operators can share transaction order flow and coordinate block building while keeping contents private until finalization.

The goal is to create a more transparent and permissionless system for MEV distribution, replacing the opaque, custom deals that currently define the market. Beaverbuild has already begun transitioning its centralized builder to this network, with additional permissionless features planned for future releases.

Beyond BuilderNet, the ecosystem has developed several complementary approaches to combat centralization and return value to users:

**Returning Value to Users:** Order flow auctions (OFAs) let users auction off their transaction flow to the highest bidder, potentially earning rebates from the MEV their trades create. The private routing solutions discussed earlier (MEV-Share, Flashbots Protect) represent one approach, while encrypted mempools hide transaction details until execution.

**Protocol-Level Protections:** Researchers are exploring MEV-smoothing (distributing MEV rewards more evenly across validators) and enshrined PBS (Proposer-Builder Separation built directly into the protocol rather than relying on external infrastructure like MEV-Boost).

**Addressing Advanced Attacks:** Time-bandit attacks, where validators reorganize recent blocks to capture MEV, are constrained by stronger finality guarantees under proof-of-stake, though related attack vectors remain an active research concern.

While these solutions show promise, results in practice remain mixed, and the arms race between MEV extraction and protection continues to evolve.

## Section V: The Cross-Domain Challenge

But even as these solutions emerge for single-chain MEV, a far larger threat looms. Just as the industry began addressing extraction within individual blockchains, a new challenge emerged that threatens to dwarf the current problems.

**Cross-Domain MEV** represents extraction strategies that span multiple blockchains simultaneously, exploiting price differences and timing advantages across separate domains.

This isn't theoretical. Advanced searchers are already executing arbitrage and other strategies across different L1s, exploiting price differences between DEXs on separate chains. The timing and latency of blockchain bridges become critical factors, enabling complex, multi-block MEV strategies that are even harder to mitigate than their single-chain counterparts.

Researchers warn it could pose severe risks (sometimes described as 'existential') to decentralization. If specialized participants gain control over transaction ordering across multiple domains, the centralization pressures described earlier could compound exponentially. The cross-domain nature makes coordination harder and value extraction more opaque, potentially creating a new class of MEV that's both more profitable and more harmful to users.

The fundamental challenge: as the ecosystem grows and interconnects, each new bridge, each new chain, each new connection creates fresh opportunities for value extraction. The solutions that work for single-chain MEV (batch auctions, private orderflow, fair ordering) become exponentially more complex when they must coordinate across multiple domains with different consensus mechanisms, block times, and economic models.

## Section VI: Key Takeaways

**MEV is intrinsic to blockchain architecture, not a bug to be eliminated.** Transaction ordering creates extractable value the moment user intent becomes visible before execution in a public mempool. This isn't a flaw that engineering can fix; it's fundamental to how decentralized systems process transactions. Your transactions are vulnerable unless you actively protect them through private routing, tight slippage controls, or batch auction mechanisms. The public mempool is a dark forest where revealing profitable intent attracts faster, more sophisticated actors.

**Not all MEV harms markets equally; distinguishing productive from predatory extraction matters.** Arbitrage enforces price consistency and prevents exploitable market divergences. Liquidations maintain protocol solvency by closing under-collateralized positions before they become bad debt. These extract value but deliver systemic benefits: tighter spreads, healthier lending markets, better capital allocation. Sandwich attacks provide no such benefits. They're pure wealth transfers that exploit information asymmetry without improving market function. This distinction matters because the same infrastructure enables both productive activities and predatory behaviors. Protocol design must account for this duality rather than treating all MEV as uniformly harmful or beneficial.

**Flashbots built infrastructure to organize extraction rather than eliminate it, creating new centralization risks.** Recognizing that extraction is inevitable, channeling competition into structured off-chain auctions reduced collateral damage by moving priority battles out of the public mempool. This made extraction more transparent and gave users protection options through private routing. Yet this efficiency came at a cost: extreme builder concentration means the solution itself became a centralization vector. A small number of operators now control block production, and their compliance decisions and technical failures affect the entire network. Making MEV extraction more efficient inadvertently created powerful gatekeepers whose centralization poses risks the protocol wasn't designed to handle.

**The economics of MEV naturally favor concentration among well-capitalized professionals.** Competitive extraction requires substantial capital, low-latency infrastructure, and specialized expertise that create natural barriers consolidating power among professional operators. The result is an invisible tax on regular users: worse execution prices, higher fees, and lost opportunities captured by faster actors. Making extraction more competitive and decentralized often means making it less efficient, creating trade-offs between censorship resistance and execution quality. Sophisticated infrastructure and capital will always have advantages in extracting ordering-based value, though better protocol design can limit concentration and reduce harm to ordinary users.

**As blockchains interconnect, MEV strategies span multiple domains simultaneously, multiplying complexity.** Cross-chain extraction exploits price differences across networks, cascading liquidations across protocols, and oracle updates creating opportunities across chains. This complicates mitigation strategies that work on single chains. Batch auctions cannot coordinate atomically across separate domains with different consensus mechanisms. The participants capable of operating at this scale represent an even smaller, more sophisticated set, raising questions about whether decentralized systems can maintain censorship resistance when extraction incentives favor increasingly powerful actors operating across the entire multi-chain landscape. Success requires balancing efficiency gains from specialization against centralization risks from concentrating power among participants who can manipulate markets at scales individual chains cannot regulate.

**MEV represents an unavoidable economic reality of blockchain architecture that protocol design can channel but never eliminate.** The public mempool creates information asymmetry, transaction ordering creates extraction opportunities, and competitive dynamics favor participants with superior capital and infrastructure. Systems that minimize harm acknowledge these forces explicitly through private routing, protocol-layer protections, and incentives that reward beneficial extraction while limiting predatory behaviors. No mechanism can perfectly separate productive from harmful MEV, and no infrastructure can fully decentralize extraction without sacrificing efficiency. Understanding MEV means accepting that sophisticated actors will always have advantages in extracting value from ordering control, and that protecting yourself requires technical awareness and recognizing that the playing field is fundamentally not level in systems where information must flow transparently.