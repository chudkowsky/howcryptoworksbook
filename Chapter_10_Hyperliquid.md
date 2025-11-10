# Chapter X: Hyperliquid

## Section I: Road to Domination

### The Great Reversal: How Hyperliquid Dethroned dYdX

In one of the most dramatic competitive reversals in DeFi history, dYdX's share of perp DEX volume fell from 75% in January 2023 to 7% by December 2024, while newcomer **Hyperliquid** rose to nearly 70% in December 2024. This transformation occurred despite dYdX's seemingly unassailable position as the established leader with years of market dominance.

The roots of dYdX's failure can be traced to flawed strategic choices that made it susceptible to being overtaken. Most critically, the project's tokenomics offered limited value to users. The original v3 version, built on StarkEx, directed all trading fees to dYdX LLC with no direct benefit to token holders. Even after migrating to v4 as a Cosmos-based appchain, the protocol's fee structure remained problematic. Trading and gas fees flowed to validators and DYDX stakers in USDC, creating no buy pressure for the native token. When the buyback program finally launched in March 2025 (presumably as a response to Hyperliquid), it only captured 25% of fees and staked the repurchased tokens rather than burning them, creating a much weaker value accrual mechanism than traditional buyback-and-burn models.

Beyond tokenomics, dYdX compounded its problems with poor execution timing. The migration to v4 introduced user friction through complex bridging requirements and increased latency to ~1-second block times, precisely when performance became critical. The timing proved disastrous, diverting critical resources to the overhaul just as Hyperliquid gained momentum.

While dYdX's token offered holders little beyond governance rights, Hyperliquid's HYPE captured value directly through aggressive buybacks. The platform conducted one of crypto's largest airdrops, distributing 31% of HYPE's total supply to over 90,000 users based on their trading activity on Hyperliquid's testnet and rival platforms like dYdX, with zero VC allocation. More importantly, Hyperliquid directs approximately 99% of trading fees toward HYPE purchases, creating an unusually tight link between trading volume and token demand. This transforms HYPE from a governance token into a claim on protocol cash flows. Fee discounts stem primarily from volume and referral tiers rather than staking requirements alone. The airdrop's initial value exceeded $1B, with HYPE surging from $4 at launch in November 2024 to nearly $60 by September 2025, reflecting the token's strong value capture.

### Technical Superiority

While dYdX struggled with its migration, Hyperliquid exploited the opening with breakthrough technology. Built as a custom L1 with a proprietary consensus mechanism, the platform achieved sub-second transaction finality with a median of 0.2 seconds. Most remarkably, it maintained a fully on-chain order book, something previously thought impossible without sacrificing performance. Unlike dYdX's hybrid approach, every bid, ask, and cancellation was recorded on-chain with transparent depth and zero gas fees for trading.

The market responded immediately and decisively. By August 2024, Hyperliquid's monthly volume first overtook dYdX. The gap then widened dramatically: by January 2025, Hyperliquid processed $200B while dYdX managed just $20B. In the second half of 2025, Hyperliquid is in a league of its own and frequently surpasses $300B in monthly volume, reaching about 15% of Binance's perp volume.

This reversal demonstrates that in crypto's fast-moving markets, superior user experience combined with aligned tokenomics can rapidly overcome established market positions, even when the incumbent enjoys years of advantage and institutional backing.

## Section II: HyperBFT and EVM

That competitive success required custom infrastructure. The platform built **HyperCore**, a bespoke L1 blockchain that prioritizes performance and accessibility while making deliberate compromises around decentralization.

### Consensus Layer: HyperBFT

**HyperBFT** powers the consensus layer, drawing inspiration from HotStuff to achieve finality under standard Byzantine assumptions (more than two-thirds honest validators). The system organizes block production through deterministic leader schedules, with epochs spanning roughly 100,000 rounds (approximately 90 minutes).

This performance comes with inherent risks in leader-based systems. If a designated leader misbehaves or goes offline, they can temporarily censor transactions until the next rotation. While validator rotation and monitoring mitigate this risk, it represents a meaningful compromise compared to leaderless consensus mechanisms.

#### Validator Economics

To become an active validator, each participant must self-delegate at least 10,000 HYPE tokens. Active validators earn the right to produce blocks and receive rewards based on their total delegated stake.

Validators can charge delegators a commission on earned rewards. However, to protect delegators from exploitation, commission increases are strictly limited: validators can only raise their commission if the new rate remains at or below 1%. This prevents validators from attracting large amounts of stake with low commissions, then dramatically increasing fees to take advantage of unsuspecting delegators.

One-day delegation locks and seven-day unstaking periods balance validator commitment with capital liquidity, though these parameters involve their own tensions between security and flexibility.

### Execution Layer: HyperEVM

**HyperEVM** addresses the accessibility challenge by providing full EVM compatibility, using HYPE as the native gas token. This allows existing Ethereum wallets, tools, and developer workflows to integrate seamlessly, a crucial factor for adoption.

#### Collateral System

USDC serves as collateral on Hyperliquid. All perpetual positions use USDC as collateral, creating a unified margin system that simplifies risk management and capital efficiency. The platform has attracted nearly $6 billion in bridged USDC from Arbitrum.

In September 2025, Circle announced it would launch a native version of USDC on Hyperliquid, starting with the HyperEVM network and expanding to HyperCore later. Circle also invested in HYPE tokens, making it a direct stakeholder in the platform. This development comes shortly after Hyperliquid held a competition to select an issuer for its native USDH stablecoin, which was won by Native Markets.

## Section III: Tradable Products

Hyperliquid's technical architecture enables three distinct trading products, each with different risk profiles and listing mechanisms.

### Product Types and Listing Mechanisms

Hyperliquid offers perps (standard perpetual futures), hyperps (pre-launch perps that use internal pricing instead of external oracles), and spot trading on fully on-chain order books. The platform also has upcoming features like permissionlessly deployed perps (HIP-3).

Listing mechanisms vary by product type. Spot listings require winning Dutch auctions to deploy HIP-1 tokens on HyperCore, then creating trading pairs through additional auctions. Perp listings are currently curated by the team with community input, though they're moving toward permissionless deployments via HIP-3. Hyperps remain curated and are specifically designed for assets without reliable external price feeds.

### Bridging and Asset Representation

All spot assets trade as HIP-1 tokens on HyperCore's L1, regardless of their origin. This includes bridged assets like Bitcoin; when a participant deposits BTC or SOL, it becomes a HIP-1 representation that trades on the on-chain order book, then can be withdrawn back to the Bitcoin or Solana blockchain.

Non-EVM assets like Bitcoin and Solana use Unit's lock-and-mint bridge, while EVM-based assets like USDC from Arbitrum use Hyperliquid's native validator-signed bridge. For Bitcoin, users send native BTC to a deposit address monitored by Unit. Once confirmed on the Bitcoin blockchain, Unit mints the corresponding HIP-1 token representation on HyperCore that can be traded. Withdrawals work in reverse: the HIP-1 token is burned and Unit releases the native BTC back to the user's address.

The bridge architecture creates meaningful security considerations. Withdrawals depend on permissioned 4-validator sets on Arbitrum (commonly summarized as 3-of-4 for the hot set), concentrating withdrawal authority in a small group of designated actors rather than being secured by the broader L1 staking consensus. This arrangement creates potential risks around fund security and withdrawal censorship if those permissioned validators were to collude or become unavailable. We'll examine these broader infrastructure dependencies in Section V.

### Hyperps: Pre-Launch Trading

Hyperps are used primarily for trading perps of tokens before they are launched, either to speculate or hedge the price of farmed proceeds. Hyperp prices remain more stable and resist manipulation compared to standard pre-launch futures. The system also provides greater flexibility; the underlying asset or index only needs to exist when the contract settles or converts, not throughout the entire trading period.

Funding rates play a crucial role in hyperp trading. When prices move strongly in one direction, the funding mechanism will heavily incentivize positions in the opposite direction for the following eight hours. This creates both opportunities and risks that traders must account for.

In August 2025, four coordinated whales executed market manipulation on Hyperliquid's XPL hyperps, profiting approximately $15M while causing over $20M in user liquidations. The attack exploited Hyperliquid's reliance on a thin, isolated spot price feed by using just $184k to artificially inflate XPL's spot price nearly eightfold, which caused the futures price to spike from $0.60 to $1.80 in minutes and triggered cascading liquidations of short positions. While technically not an exploit since it operated within the protocol's design, the attack exposed critical vulnerabilities in hyperps. This prompted Hyperliquid to implement emergency safeguards including 10x price caps.

### Liquidation Transparency and Risks

Full on-chain verifiability means positions and liquidation thresholds can sometimes be inferred from public state and trading behavior. While that visibility improves auditability and market integrity, it also makes clustered liquidations easier to target: adversaries can strategically push mark prices through known liquidity-light levels to trigger cascades, imposing outsized losses on passive participants. These liquidation risks fall heavily on HLP depositors, as we'll see in the next section. Mitigations include tighter per-asset risk limits and position caps, anti-manipulation bands around liquidation prices, staggered or batched liquidation flows, and circuit breakers.

## Section IV: The HLP Design

With tradable products in place, Hyperliquid faced another challenge: ensuring the liquidity depth necessary for these markets to function. Technical performance alone doesn't guarantee success; traders demand deep liquidity, tight spreads, minimal slippage, and reliable liquidation mechanisms, requirements that have historically favored centralized exchanges with dedicated market makers. Hyperliquid's solution creates new compromises between liquidity provision and risk concentration.

**The Hyperliquidity Provider (HLP)** represents Hyperliquid's most innovative design choice: a community-owned vault that simultaneously provides market-making services and handles liquidations. Depositors contribute capital to HLP and share in its profit and loss, creating a decentralized market-making system that doesn't rely on external firms. HLP's profits come primarily from market-making spreads and liquidation fees, while losses stem from adverse selection when sophisticated traders exploit market inefficiencies and from holding losing positions as the counterparty to winning trades.

This design solves several problems at once. HLP provides consistent liquidity across all markets, handles liquidations efficiently (crucial for leveraged trading), and distributes market-making profits to the community rather than extracting them to external firms. The system internalizes much of the trading flow, reducing the need for external counterparties.

However, this concentration creates meaningful risks. During extreme volatility, HLP depositors bear the losses from adverse selection and liquidation cascades. While HLP isn't the sole counterparty on the CLOB (anyone can post liquidity), it provides core baseline liquidity across markets and performs liquidations, creating concentration risk that traditional market-making structures distribute across multiple firms.

The **JELLY** manipulation in March 2025 demonstrated how vault-based systems can suffer losses from coordinated attacks. Attackers opened large leveraged positions ($4.5M short, two $2.5M longs) on a low-liquidity token JELLY, then manipulated the liquidation process while simultaneously pumping the token's price 250% on Solana. This created a $12 million unrealized loss that threatened the protocol's solvency. Validators had to make an emergency intervention, overriding the oracle price to prevent collapse, while the team quickly implemented fixes including better position size limits, improved liquidation mechanisms, and enhanced governance controls. All traders were compensated, but the incident exposed significant vulnerabilities in the platform's risk management architecture.

## Section V: The Decentralization Challenge

These product-level risks exist within a broader infrastructure that itself involves trade-offs. While Hyperliquid's technical performance enabled its rapid growth, that execution efficiency required calculated centralization choices. Understanding these limitations is essential for evaluating the platform's long-term viability.

### Validator Control and Operations

The most prominent concern centers on validator control, where the Hyper Foundation controls approximately 80% of staked HYPE through its own validators. The Foundation serves as the protocol's primary steward, responsible for core development, infrastructure maintenance, and ecosystem grants, while holding significant token reserves to fund long-term operations. This concentration could theoretically allow a single entity to halt or steer the chain, raising questions about censorship resistance.

The validator experience itself has drawn significant scrutiny. The protocol relies on closed-source node software, forcing validators to run what critics describe as a "single binary" with limited documentation. Validators have publicly complained that this arrangement creates a "blind signing" scenario where they cannot inspect the code they're running, leading to frequent jailing incidents and making it difficult to assess risks independently. The validator selection process has also faced criticism for being opaque, with reports of low rewards relative to self-bonding requirements and the emergence of a testnet HYPE black market.

### Infrastructure Dependencies

Infrastructure dependencies present additional risks that have manifested in real-world disruptions. Hyperliquid's architecture relies heavily on centralized APIs for both validator operations and user access. Validators reportedly need to call Hyperliquid-operated APIs to recover from jailing, while users depend on these same API servers to submit transactions and access market data. This dependency became acutely apparent during a July 2025 incident when API traffic spikes caused 37 minutes of trading disruption, effectively freezing user interactions despite the underlying blockchain continuing to produce blocks.

### The Path Forward

Hyperliquid has acknowledged these concerns and indicated plans to open-source code and decentralize infrastructure over time. The current architecture reflects a strategic choice to prioritize rapid iteration and security hardening in the protocol's early stages, gradually relinquishing control as the system demonstrates resilience at scale.

## Section VI: The Governance Balance

With liquidity mechanisms in place, Hyperliquid faced a strategic question: how to enable permissionless expansion while maintaining quality and managing risk. The protocol's governance system addresses this through economically-enforced quality controls.

**Hyperliquid Improvement Proposals (HIPs)** govern platform evolution, with each proposal addressing specific aspects of permissionless expansion:

HIP-1 established a native token standard with a 31-hour Dutch auction mechanism, allowing anyone to list spot tokens. This democratizes token launches while using a 31-hour Dutch auction to set deployment gas/ticker costs, which raises the bar for drive-by launches since the auction format naturally selects for tokens with genuine demand.

HIP-2 introduced automated "Hyperliquidity" for spot pairs against USDC, ensuring baseline liquidity for newly listed HIP-1 tokens. This solves the chicken-and-egg problem where tokens need liquidity to attract traders, but they need traders to justify liquidity provision.

HIP-3 (only live on testnet) aims to make perpetual markets permissionless, subject to a 1 million HYPE staked requirement by the deployer. Builders receive a share of fees in return. This creates strong incentives for responsible listings while generating meaningful cost for spam or low-quality markets.

The 1 million HYPE requirement effectively limits perpetual launches to serious participants while aligning their incentives with market success. However, builders face validator-driven delisting and potential stake slashing for malicious or unsafe operation, effective for quality control but can discourage experimentation.

This governance structure reflects how protocols can decentralize without sacrificing quality: economic stakes create market-driven curation where builders must justify capital allocation upfront. Pure permissionlessness leads to noise and poor user experience; high barriers ensure serious participants while potentially discouraging experimentation. It's a calculated compromise that prioritizes ecosystem quality over absolute openness.

## Section VII: Emerging Competitors

Hyperliquid's dramatic rise, frequently surpassing $300B in monthly volume by late 2025, validated the perpetual DEX thesis and painted a target on its back. The sector reached nearly $630 billion in monthly trading volume across at least twenty competing protocols. This growth has attracted both capital and competitive scrutiny. Established projects have pivoted toward perps, and well-funded newcomers have launched with differentiated strategies designed to challenge the leader.

Two protocols have emerged with particularly distinct approaches to challenging Hyperliquid's position.

**Lighter: Verifiable Security Architecture**

**Lighter** markets itself as the security-first alternative, built as a zk-rollup whose custom ZK circuits generate cryptographic proofs for order-matching and liquidations. The protocol launched its public mainnet in early October 2025 on an Ethereum L2, with user collateral remaining custodied on Ethereum itself, a design choice detailed in its whitepaper that prioritizes asset security over raw performance. Lighter claims to be the first exchange to offer verifiable matching and liquidations, a security focus supported by external audits including zkSecurity's circuit audit and recent Nethermind Security audits covering core contracts and bridge infrastructure.

The platform's fee structure targets retail traders: standard users trading through the front end pay zero maker and taker fees, while API access and high-frequency trading flow incur charges. Funding payments remain peer-to-peer between longs and shorts rather than platform fees. This fee structure appeals to institutional and risk-conscious traders who prioritize verifiable safety in a landscape where, as perpetual DEXs achieve CEX-like responsiveness and deeper liquidity, attack surfaces expand proportionally. In this context, cryptographic verification becomes a competitive differentiator rather than merely a baseline feature.

**Aster: The Binance-Connected Challenger**

**Aster** takes a markedly different approach, emerging from the merger of Astherus and APX Finance with backing from YZi Labs (CZ's venture firm) and CZ serving in an advisory capacity. Binance has clarified it holds no official role, though the connection to its founder and former executives provides significant credibility and network effects.

The platform's business model combines competitive fee structures (starting around 0.01% maker and 0.035% taker with VIP tiering and a 5% discount for paying fees in $ASTER tokens) with the "Trade and Earn" model that allows yield-bearing assets like USDF (Aster's own fully-collateralized stablecoin, with variable APY promoted around 17% during Season 2) and asBNB to serve directly as collateral.

Product features target diverse trader segments. Hidden Orders conceal position sizes for privacy-conscious traders, while dual trading modes serve both novices (Simple mode with up to 1001× leverage) and professionals (Pro mode with advanced tools). Beyond crypto perpetuals, Aster has expanded into leveraged stock perpetuals in Pro mode, broadening its addressable market.

Reported metrics suggest significant traction: approximately $500 billion in cumulative volume, fees of over $110 million, and 1.8 million user addresses. However, these figures warrant scrutiny. DefiLlama temporarily delisted Aster's perpetual volumes amid wash-trading concerns, and data quality debates remain ongoing. The platform operates with a hybrid architecture (off-chain matching engine paired with on-chain settlement) that enables faster execution while maintaining non-custodial asset security, though it may limit appeal to DeFi purists seeking fully decentralized infrastructure.

Aster continues to run intensive incentive campaigns, with its Genesis/Dawn points program (Stage 3 currently live) designed to bootstrap liquidity and user adoption.

## Section VIII: Key Takeaways

**Tokenomics determine competitive outcomes more than technical superiority alone.** dYdX's share of perp DEX volume collapsed from 75% to 7% despite years of leadership. This was largely because it never gave users a compelling reason to hold DYDX tokens. Hyperliquid understood this from day one, directing the majority of trading fees toward HYPE buybacks and distributing a significant portion of supply via airdrop with minimal VC allocation. This transformed HYPE from a governance token into a claim on protocol cash flows. The lesson extends beyond perpetual DEXs: protocols that treat tokens as afterthoughts will lose to competitors who align incentives from launch, regardless of technical advantages.

**Building for performance first, decentralizing as the protocol matures.** Hyperliquid achieved sub-second finality and fully on-chain order books through HyperBFT, execution efficiency that helped it grow quickly. This required deliberate tradeoffs that prioritize rapid iteration and security hardening in the protocol's early stages. The API outage that temporarily froze trading highlighted areas for improvement. As Hyperliquid matures and proves its security model at scale, the team can progressively decentralize by expanding the validator set, opening source code, and distributing stake more broadly. This staged approach lets the foundation move fast, learn from real-world stress tests, and gradually relinquish control as the system demonstrates resilience.

**HLP bootstrapped liquidity while the protocol finds sustainable solutions.** HLP solved the cold-start problem by letting depositors collectively provide market-making and handle liquidations, enabling Hyperliquid to launch competitive markets quickly. This was an intentional design choice for the early stage, though it concentrates risk on retail users rather than professional firms with diversified books. The JELLY incident, which created significant unrealized losses and required emergency validator intervention, and the XPL attack that exploited transparent on-chain positions, revealed the limitations of this approach. These events are valuable stress tests that inform the protocol's evolution. As Hyperliquid matures and attracts more market makers, HLP's role will naturally shift from primary liquidity provider to a backstop for new or less liquid markets. The team can develop additional mechanisms like private market-making vaults, tiered risk structures, or hybrid models that distribute risk more effectively while maintaining the on-chain transparency that makes the protocol valuable.

**Permissionless expansion requires sophisticated economic barriers, not just technical ones.** Hyperliquid's HIP framework demonstrates how protocols can decentralize without sacrificing quality: HIP-1's Dutch auctions naturally filter spam by making deployers compete for listings, HIP-2's automated Hyperliquidity solves the chicken-and-egg problem for new tokens, and HIP-3's substantial staking requirement ensures perpetual deployers have skin in the game. This approach recognizes that unrestricted deployment without economic filters devolves into ecosystem pollution that degrades the user experience; economic stakes create market-driven curation where builders must justify capital allocation upfront and face validator-driven delisting for malicious behavior. The trade-off is real. High barriers discourage experimentation, but platforms that mistake openness for value creation will fragment liquidity across worthless markets.

**Competition in perpetual DEXs now bifurcates along security versus network effects.** The sector has reached massive monthly volumes across multiple competing protocols, with challengers attacking Hyperliquid from opposite angles. Lighter bets that institutional traders will pay for cryptographic verification, offering zk-rollup architecture with Ethereum-custodied collateral and zero frontend fees for retail, while Aster leverages CZ's network and intensive incentives to target volume maximalists who prioritize execution efficiency and novel features over decentralization purity. Neither approach directly replicates Hyperliquid's balance; Lighter sacrifices performance for verifiable security, Aster sacrifices credibility for growth hacking. The winner will depend on whether users ultimately care more about not getting hacked or about feeling like they're using the next Binance.

The perpetual DEX race ultimately reveals that **builders must choose their centralizations carefully, because all performance gains require trust trade-offs somewhere.** Hyperliquid chose validator concentration and closed-source infrastructure; Lighter chose zk-rollup latency; Aster chose Binance adjacency and off-chain matching. None of these are pure decentralization. They're different bets on which trust assumptions users will accept in exchange for execution efficiency, security, or network effects. As the sector matures and volumes approach centralized exchange levels, the protocols that survive will be those whose chosen centralizations align with user priorities and regulatory realities, not those claiming to have solved the impossible trilemma.