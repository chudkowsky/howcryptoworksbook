# Chapter VII: MEV

Control over transaction ordering creates and redistributes value on‑chain. This chapter connects market microstructure to MEV: who extracts it, how it impacts users, and what mitigations (private order flow, batch auctions, PBS) can return value or reduce harm.

## Section I: The Market Chaos: Understanding MEV Fundamentals

Picture a busy marketplace with a peculiar setup: there's a big whiteboard where everyone must post their intended purchases before they can buy anything. You write "buying 10 tomatoes from Stall A," and suddenly chaos erupts.

A fast-moving reseller spots your order, sprints to Stall A, buys the tomatoes first, then offers them back to you at a markup. Another reseller notices you're about to make a large purchase that will drive up tomato prices, so they buy just before you and sell immediately after, pocketing the price difference your trade created. Meanwhile, the market manager starts auctioning off the right to decide who gets served first: whoever pays the highest tip jumps to the front of the line.

This market chaos isn't just an analogy but rather exactly what happens in **the public mempool** (and increasingly in private order-flow auctions), creating what researchers call a "dark forest" where revealing profitable trades attracts predators.

**Maximal Extractable Value (MEV)** is the profit that emerges from this system. Originally called "Miner Extractable Value" during Ethereum's proof-of-work era, MEV represents revenue extracted beyond standard block rewards and transaction fees by strategically ordering, including, or excluding transactions within blocks.

In our market analogy, the key players have clear roles: **searchers** are the fast-moving resellers scanning for opportunities, **builders** are market managers who construct blocks and **bid their value to proposers via MEV-Boost**, and **proposers** (validators) are the market owners who choose which manager's arrangement to accept. This relationship has been formalized through systems like **MEV-Boost**, which creates a liquid market for block space by essentially letting market managers bid for the right to organize transactions.

The fundamental insight is that MEV arises from controlling transaction visibility and ordering. Some activities (like ensuring prices stay aligned across different stalls or liquidating bad debt) can stabilize the market, but the overall effect imposes an implicit tax on regular shoppers through worse execution and externalities while only well-funded professionals with the fastest runners and private backroom deals consistently win.

This creates the core tension: how transaction ordering, designed to be neutral infrastructure, becomes a sophisticated value extraction mechanism that threatens the very decentralization it's meant to serve.

## Section II: How Value Gets Extracted

The strategies that emerge from this environment follow a predictable escalation. The simplest is **arbitrage**: buying an asset at a lower price on one exchange to sell it at a higher price on another. This actually helps the market by keeping prices aligned across different venues, but when competition heats up, searchers get more aggressive.

They start **front-running**, copying your transaction but paying extra to go first. For example, when you spot an arbitrage opportunity where you can buy ETH for $3,000 on one DEX and immediately sell it for $3,050 on another DEX, a bot sees your transaction and submits the exact same arbitrage trade with higher gas fees to capture that $50 profit before you can.

Then comes the **sandwich attack**: they buy before you (driving up the price), let you buy at the inflated rate, then immediately sell at the higher price you created, capturing a near‑riskless profit when their bundle lands as planned. For example, you try to swap 10 ETH for a token at $100 per token, but a bot buys first pushing the price to $105, your trade executes at $105, then the bot immediately sells their tokens back at $104, pocketing the $4-5 spread they created by sandwiching your transaction.

**Liquidations** represent another category: when someone's borrowed too much against their collateral, searchers race to claim the reward for closing out the position. Unlike sandwiching, liquidations serve a necessary function, but the race to claim them still inflates costs for everyone.

The market impact creates a fundamental tension between efficiency and fairness. While arbitrage enhances price discovery and liquidations maintain protocol health, the overall MEV ecosystem extracts an **"invisible tax"** from users. 

Priority-gas-auction bidding historically spiked gas costs as bots competed for transaction priority; today much of that competition is **off-chain via order-flow and builder auctions**, reducing broad mempool fee spikes but often shifting costs into worse execution for users or rebates captured by intermediaries. This isn't just theoretical harm. Every sandwich attack represents value directly transferred from a user to a sophisticated actor, even if the fee externalities now appear less in the public mempool and more in private routing markets.

The response has been innovation in execution methods. **Frequent batch auctions** and **intent-based settlement** (like CoW Swap and Uniswap X) **remove the continuous-time priority that enables classic sandwiching**. Instead of processing trades one-by-one in a race, these systems collect orders and execute them together, greatly reducing the timing games that create MEV opportunities. While batch auctions effectively mitigate sandwiching attacks, they don't eliminate all forms of MEV such as liquidations or oracle-based extraction.

## Section III: Flashbots: Taming the Dark Forest

By 2020, Ethereum faced exactly this market chaos at scale. The priority gas auctions described earlier were creating network congestion, while miners were capturing MEV through opaque, off-chain deals that favored sophisticated actors.

Enter **Flashbots**, a research organization founded in 2020 with a radical proposition: instead of trying to eliminate MEV, create transparent infrastructure to make it more fair and efficient. Their insight was that MEV extraction was inevitable, but the current system was wasteful and harmful to regular users.

**MEV-Geth and the First Solution**: In January 2021, Flashbots released **MEV-Geth** (a modified Ethereum client) with **mev-relay**, creating a private communication channel between searchers and miners. Instead of competing in the public mempool with escalating gas bids, searchers could submit transaction bundles directly to miners through this sealed-bid auction system. This moved the competition off-chain, reducing PGA spam in the public mempool.

The system worked like creating a separate, organized auction house for our market resellers. Instead of everyone shouting bids in the main marketplace (causing chaos for regular shoppers), the resellers could submit sealed bids to market managers who would choose the most profitable arrangement. This reduced the chaos in the main marketplace while sophisticated actors could still compete for MEV opportunities.

**The Transition to Proof-of-Stake**: When Ethereum moved to proof-of-stake in September 2022, the entire MEV landscape needed rebuilding. Flashbots developed **MEV-Boost**, an open-source middleware that provides **out-of-protocol Proposer-Builder Separation (PBS)**. This expanded the builder-validator relationship introduced earlier into a full competitive marketplace via **relays**. Today, approximately 85-95% of Ethereum blocks are built via MEV-Boost.[^2] Note that this is distinct from **enshrined PBS**, which remains in development and research phases.

The system evolved from individual miners making direct deals to a sophisticated auction where multiple builders compete for validator selection, with relays facilitating the bidding process.

**User Protection Through Flashbots Protect**: Recognizing that infrastructure alone wasn't enough, Flashbots launched Flashbots Protect, a service that routes user transactions through private mempools. This shields regular users from the MEV extraction strategies detailed earlier while potentially providing rebates from captured MEV. The service works by bypassing the public mempool and reducing sandwich/frontrunning risk. These transactions still compete in the builder auction but are not exposed to public mempool predation.

The Flashbots approach represents a pragmatic philosophy: since MEV extraction is inevitable in any system with transaction ordering, the goal should be making it transparent, efficient, and less harmful to users. Rather than fighting the economic forces, they built infrastructure to channel them constructively.

## Section IV: The Centralization Crisis

Despite Flashbots' innovations, the MEV ecosystem still creates a brutal reality: success in MEV requires both deep pockets and technical expertise. You need capital to compete in liquidation auctions, sophisticated infrastructure to detect opportunities faster than competitors, and the technical knowledge to navigate an increasingly complex landscape. The result? Dangerous concentration.

In 2024, block building was highly concentrated; for example, in mid-October two builders produced ~89% of blocks over a two-week window, and from October 2023 through March 2024 three builders produced ~80% of MEV-Boost blocks. Over the same period, a sizable share of blocks were relayed via OFAC-compliant infrastructure, often around 40 to 60% (and sometimes higher) depending on the measurement window. The pattern is clear: a small number of sophisticated actors dominate MEV extraction, undermining the decentralized ethos of blockchain networks.

This concentration sparked innovation. In 2024, major players announced **BuilderNet**, a decentralized block-building network launched Nov 2024 and jointly operated (at launch) by Flashbots, Beaverbuild, and Nethermind. BuilderNet uses **Trusted Execution Environments (TEEs)** to allow multiple operators to share transaction order flow and coordinate block building while keeping contents private until finalized. Think of it as allowing multiple market managers to collaborate on organizing the optimal serving order without revealing their strategies to competitors.

This architecture aims to create a more transparent and permissionless system for MEV distribution, moving away from the opaque, custom deals that define the current landscape. Beaverbuild is already transitioning its centralized builder to this new network, with more permissionless features planned for future releases.

The broader toolkit approach recognizes that different participants need different strategies. **Order flow auctions (OFAs)** and **private orderflow** solutions (like MEV-Share, SUAVE, private relays, and encrypted mempools) seek to return value to users through rebates, though results in practice remain mixed. **Time-bandit attacks** (reorganizing blocks to capture MEV) are constrained by stronger finality guarantees (and are rarer under PoS than PoW), though related vectors remain an active research concern, while researchers explore **MEV-smoothing** and **enshrined PBS** (Proposer-Builder Separation) to further distribute value extraction.

**Operational notes:** Prefer intent/batch‑auction settlement for retail orderflow to eliminate sandwich windows. Enforce simulation, slippage bounds, and pause hooks at the protocol level to reduce exploit surfaces.

## Section V: Cross-Domain MEV

Just as the industry began addressing single-chain MEV, a new challenge emerged that threatens to dwarf the current problems. **Cross-Domain MEV** extends our market analogy: imagine if the resellers could now sprint between multiple adjacent markets, buying low in Market A and selling high in Market B faster than anyone else could react.

This isn't theoretical. Sophisticated actors are already executing arbitrage and other strategies across different L1s, exploiting price differences between DEXs on separate chains. The timing and latency of blockchain bridges become critical factors, enabling complex, multi-block MEV strategies that are even harder to mitigate than their single-chain counterparts.

Researchers warn it could pose **severe risks** (sometimes described as 'existential') to decentralization. If sophisticated actors gain control over transaction ordering across multiple domains, the centralization pressures we've seen on individual chains could compound exponentially. The cross-domain nature makes coordination harder and value extraction more opaque, potentially creating a new class of MEV that's both more profitable and more harmful to users.

The challenge is that as the blockchain ecosystem grows and interconnects, each new bridge, each new chain, each new connection creates fresh opportunities for value extraction. The solutions that work for single-chain MEV (batch auctions, private orderflow, fair ordering) become exponentially more complex when they must coordinate across multiple domains with different consensus mechanisms, block times, and economic models.

Mitigations under study include **shared sequencing** across domains (with projects like Espresso and Astria in active rollout and testing phases), **cross-domain batch auctions**, and **routing intents through OFAs** that can coordinate across chains. Solutions like SUAVE are currently in testnet/alpha phases rather than production mainnet. However, these solutions are still largely experimental, and the race between MEV extraction and mitigation continues to intensify.

## The Ongoing Battle for Fair Markets

The MEV challenge illustrates a broader truth about decentralized systems: technical solutions create new economic realities, which create new technical challenges. What began as a simple ordering problem has evolved into a sophisticated ecosystem that threatens the very decentralization it was meant to preserve.

Yet the response has been equally sophisticated. From private orderflow to batch auctions, from BuilderNet to cross-domain coordination, the ecosystem continues to innovate. The market analogy that opened this chapter remains apt: just as physical markets developed regulations, clearing houses, and fair trading practices over centuries, blockchain markets are rapidly evolving their own mechanisms for fair value distribution.

The stakes couldn't be higher. MEV extraction that benefits sophisticated actors at the expense of regular users undermines the promise of decentralized finance. But the solutions emerging (intent-based systems, private execution, fair ordering mechanisms) point toward a future where the benefits of programmable money can be realized without the extractive dynamics that plague traditional finance.

As blockchain networks multiply and interconnect, the next chapter of this story is already being written across domains and chains. The question isn't whether MEV will continue to evolve, but whether the mitigations can keep pace with the extraction.