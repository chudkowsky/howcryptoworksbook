# Chapter 4 - L1 Blockchains

When builders talk about **Layer 1 blockchains**, they're referring to the foundational networks that provide the base layer of blockchain infrastructure - Bitcoin, Ethereum, Solana, and dozens of others competing for developers, users, and capital. But what exactly makes an L1, and why do we have so many different approaches?

Every L1 is fundamentally a bundle of four core functions: **execution** (processing transactions), **settlement** (finalizing state), **consensus** (agreeing on order and validity), and **data availability** (ensuring transaction data is accessible). How these functions are organized - whether tightly integrated in a single chain or distributed across specialized layers - represents one of the most important architectural decisions in blockchain design. For instance, Bitcoin prioritizes simplicity and ironclad security for digital money, while Ethereum and Solana embrace greater complexity to enable programmable applications and high-throughput execution.

The core thesis of this chapter is simple: every blockchain design involves trade-offs, and competition between L1s is as much about **liquidity, infrastructure, and attention** as it is about raw technical performance. A chain might process 100,000 transactions per second, but if it lacks users and developer, those transactions flow elsewhere. In fact, by 2025 it's become clear that there is more available blockspace spread across tens if not hundreds of L1s than there is demand to fill it.

This chapter connects the deep technical dives from our earlier explorations of Bitcoin, Ethereum, and Solana (Chapters I-III) with the market dynamics we'll examine later - from MEV and market structure (Chapters VI-VII) to DeFi ecosystems and governance (Chapters VIII-XII). Understanding L1 architecture provides the foundation for everything else in the crypto stack.

## Section I: Blockchain Architectures

### The Four Planes

Think of a blockchain as a restaurant that needs to handle four essential functions. **Execution** is the kitchen - where orders (transactions) get processed and meals (state changes) get prepared. **Settlement** is the dining room - where completed meals get delivered and customers pay their bills (finalized state). **Consensus** is the management system - ensuring everyone agrees on which orders came first and which tables they belong to. **Data availability** is the record-keeping - maintaining receipts and records so anyone can verify what happened.

The **modular blockchain thesis** argues these functions don't need to live together. Why force the same nodes to handle lightning-fast trading execution and long-term data storage? Specialized layers can optimize for specific functions:
- **Execution layers** can focus purely on transaction processing
- **Settlement layers** can provide economic finality and dispute resolution  
- **Consensus layers** can optimize for fast, secure block production
- **Data availability layers** can efficiently store and distribute transaction data

**Monolithic blockchains** integrate all four functions into a single layer, creating what advocates call "local composability." When everything happens on the same chain, smart contracts can interact with each other atomically - either all related transactions succeed together, or they all fail together. This makes building complex DeFi protocols much simpler.

The monolithic trade-off becomes apparent in operational requirements. High-throughput monolithic chains often demand specialized hardware, fast networking, and sophisticated operational expertise. As transaction volume grows, validator requirements increase, potentially limiting the number of entities that can practically run full nodes. 

Decentralization in practice exists on a spectrum; there is no crisp threshold for being 'decentralized enough.' A pragmatic lens is the cost and coordination required to shut the network down - economically, legally, and operationally. In practice, Solana supporters believe the chain is decentralized enough, while Ethereum supporters generally disagree. You see effectively the same effect with Bitcoiners, who consider Ethereum too centralized.

### Modular Architectures

Blockchain **modularity** represents a fundamental shift from monolithic designs toward specialized, interoperable components. Rather than handling execution, consensus, settlement, and data availability within a single system, modular architectures unbundle these functions to optimize each independently. Most real-world implementations exist along a spectrum between pure monolithic and pure modular approaches.

**Ethereum's evolution** exemplifies this transition. The network's **rollup-centric roadmap** transforms Ethereum into a modular base layer where **Layer 2 rollups** handle transaction **execution** while **Ethereum L1** specializes in **settlement** (verifying proofs and resolving disputes) and **consensus**. This division of labor allows each layer to optimize for its specific role - rollups for throughput and cost, Ethereum for security and finality.

**Data availability** has emerged as a critical design choice for rollups. Many use Ethereum directly through **EIP-4844 blobs**, which introduced a separate **blob-gas fee market** distinct from regular transaction fees. These blobs store data temporarily, pruning it after approximately 18 days - sufficient for challenge periods and fraud proofs without permanent on-chain storage. The **Dencun upgrade** implementing this system delivered dramatic cost reductions, with many **L2s** seeing 65-95% savings on data availability expenses.

However, modularity enables choice. Some rollups opt for alternative **data availability layers** like **Celestia** or **EigenDA** while maintaining **Ethereum settlement**. This approach potentially reduces costs further but involves trade-offs in **L1-equivalence** and **exit security**, as users must trust additional systems beyond Ethereum itself.

Other ecosystems approach modularity differently. **Avalanche** takes yet another approach with **subnets** - sovereign chains secured by their own validator sets. While validators historically joined the Primary Network, the **Etna upgrade** relaxes this requirement for new **L1 networks**. Crucially, **subnets do not automatically inherit** the Primary Network's security; each maintains independent validator economics and security guarantees, creating a federation of specialized chains rather than a shared security model.

### Key Trade-offs

The architectural choice between monolithic and modular approaches represents one of the fundamental fault lines in current L1 design philosophy. The **composability trade-off** highlights the core tension. Monolithic chains offer **local composability** - complex multi-step transactions that either succeed or fail atomically. Modular architectures require **cross-layer composability** - coordinating actions across multiple chains with different finality timings and trust assumptions. 

Building a flash loan that arbitrages between multiple DeFi protocols is trivial on a monolithic chain but complex across rollups. The arbitrage might succeed on one rollup but fail on another, leaving the user with unwanted positions. **Atomicity across rollups generally isn't possible without extra trust/coordination (shared sequencers, intents, etc.)**, which are still maturing. The complexity remains higher than single-chain development.

## Section II: Consensus & Finality

### Proof-of-Work vs Proof-of-Stake

Understanding how blockchains reach agreement is crucial for evaluating their security and performance characteristics. **Proof-of-Work** systems like Bitcoin use computational puzzles to select block producers, while **Proof-of-Stake** systems like Ethereum use economic stake for the same purpose.

PoW provides **probabilistic finality** - each additional block makes reversal exponentially more expensive, but reversal remains technically possible given sufficient computational power. Think of it like adding locks to a safe: each lock makes theft harder, but a sufficiently motivated attacker with enough resources could theoretically break through.

PoS systems can provide faster and sometimes stronger finality guarantees. **Ethereum's Casper FFG** creates **economic finality** - after certain checkpoints, reversal would require destroying at least one-third of all staked ETH (currently worth tens of billions of dollars). This makes reversal not just computationally expensive but economically catastrophic for attackers.

### BFT Consensus Families

Many newer chains use **Byzantine Fault Tolerance (BFT)** consensus algorithms that provide **deterministic finality (usually seconds)** when <1/3 of voting power is faulty - once a block is confirmed, it's immediately and permanently final. If **>1/3** goes offline, the chain **halts** rather than risks safety.

**Tendermint** (used by Cosmos and many app-chains) requires validators to reach consensus before producing each block. Liveness requires ≥2/3 voting power online, so **>1/3 offline** can halt progress. The trade-off: slower transaction processing for deterministic finality.

**HotStuff-style consensus** (used by Aptos and Diem) aims to improve on Tendermint's performance while maintaining safety guarantees. These algorithms use pipelining and optimizations to achieve higher throughput while preserving BFT properties.

**Solana's Proof-of-History** creates a different approach altogether. PoH provides a cryptographic clock; consensus is Tower BFT (a PoH-clocked BFT protocol). Users often act on optimistic confirmations (~400ms slots), while *finalized* commitments arrive after additional votes. This enables very high throughput with predictable timing.

### Finality Types and Trade-offs

**Probabilistic finality** (Bitcoin-style) means reversal becomes exponentially less likely over time but never reaches zero probability. Six confirmations provide very high confidence, but large transactions might wait for more confirmations during periods of high uncertainty.

**Economic finality** (Ethereum-style) means reversal would require destroying significant economic value, making attacks economically irrational. However, this assumes rational attackers - nation-state or ideologically motivated attacks might accept economic losses.

**Deterministic finality** (BFT-style) means finality arrives within seconds and is mathematically guaranteed, assuming less than one-third of validators are malicious. The trade-off usually involves lower throughput or higher centralization pressure.

These differences have practical implications. **DeFi protocols** might wait 6-12 blocks on Bitcoin. On Ethereum, some apps act on 1-2 block confirmations for UX, but *economic finality* arrives after ~2 epochs (~12.8 minutes). BFT chains can provide deterministic finality. **Cross-chain bridges** need to take these finality models into account to calibrate security parameters appropriately.

### Liveness vs Safety

The **CAP theorem** is loosely analogous to blockchains - practically a safety vs. liveness trade-off under partitions. Systems face tensions between **liveness** (continuing to produce blocks) and **safety** (never producing invalid or conflicting blocks).

**Bitcoin** prioritizes liveness - the network continues producing blocks even during significant partitions, though temporary forks may occur. **Ethereum** post-Merge has an "inactivity leak" mechanism that gradually reduces the stake of offline validators, eventually allowing the online portion to maintain liveness.

Many **BFT chains** prioritize safety - they halt if more than one-third of validators go offline, preventing any possibility of producing conflicting blocks. This provides stronger safety guarantees but can create availability risks during network partitions or coordinated attacks.

Understanding these trade-offs helps explain why different chains make different design choices based on their intended use cases and threat models.

## Section III: Virtual Machines & Programming Models

### The EVM Gravity Well

The **Ethereum Virtual Machine (EVM)** has created an enormous ecosystem gravity well. Thousands of developers know Solidity, hundreds of projects have been audited, and countless tools exist for testing, debugging, and deploying EVM bytecode. This creates powerful network effects that extend far beyond Ethereum itself.

**EVM-compatible chains** like BNB Smart Chain (BSC), Monad (emerging), Avalanche C-Chain, and Polygon can instantly inherit this entire ecosystem. Uniswap-style contracts can be deployed with minimal changes on these networks, bringing battle-tested DeFi protocols to new environments with different performance or cost characteristics.

**EVM limitations** become apparent at scale. Sequential execution means complex transactions can block simpler ones, gas price volatility creates unpredictable costs, and the lack of native parallel execution limits throughput. Various EVM implementations add optimizations, but fundamental architectural constraints remain.

### Parallel Execution: The SVM Approach

As detailed in Chapter III, **Solana's Sealevel Virtual Machine (SVM)** revolutionizes blockchain execution through **parallel processing**. By requiring transactions to declare **account access** upfront, SVM enables concurrent execution of non-conflicting transactions, significantly boosting throughput. Its **account ownership model** enhances security by preventing many reentrancy attacks.

The success of **SVM's design** has attracted attention from new blockchain projects. Networks like **Solayer** and **Fogo** are building entirely new **L1 blockchains** on top of the SVM architecture. **Fogo** takes this further by attempting to maximize SVM performance through a **permissioned validator set** running exclusively the **Firedancer client** with **multi-local consensus** - essentially pushing the SVM model to its theoretical limits in a controlled environment.

### Move: Safety Through Language Design

**MoveVM** (used by Aptos and Sui) takes a different approach by building safety directly into the programming language. Move treats digital assets as **resources** - objects that cannot be copied or accidentally destroyed, only moved between accounts.

Move's linear types prevent accidental duplication/destruction of resources, helping avoid entire classes of bugs like double-spending through programming errors. However, mint/authorization policies still depend on how modules are written. Resources can only exist in one place at a time and must be explicitly consumed or stored.

**Sui's object model** pushes this further by treating everything as objects with unique identifiers. Transactions can operate on disjoint sets of objects in parallel, enabling very high throughput while maintaining safety guarantees. Simple transfers touching different objects can process in parallel, while complex transactions touching shared objects coordinate through consensus.

### WASM and Emerging VMs

**WebAssembly (WASM)** provides a compilation target that enables multiple programming languages on the same blockchain. **CosmWasm** (used in the Cosmos ecosystem) allows developers to write smart contracts in Rust that compile to WASM.

**NEAR Protocol** uses WASM for its contract execution, with contracts commonly written in Rust or JavaScript/AssemblyScript, while maintaining an account model familiar to Ethereum developers. This provides performance benefits of compiled code while preserving developer experience patterns from the EVM ecosystem.

**Polkadot's** substrate framework also uses WASM for runtime logic, enabling chains to upgrade their core logic without hard forks. This creates powerful upgrade mechanisms but adds complexity to the development and deployment process.

### Development Experience Trade-offs

The choice of **virtual machine** significantly shapes the **developer experience** and ecosystem growth potential. The **Ethereum Virtual Machine (EVM)** enjoys notable advantages built over years of development and adoption. Its **mature tooling ecosystem** includes battle-tested frameworks like **Hardhat**, **Truffle**, and **Remix** for development and testing, while **extensive documentation** provides years of accumulated knowledge, examples, and best practices. Perhaps most importantly, the EVM benefits from a **large auditor pool** with many security firms specializing in **Solidity** reviews, and robust **composability** that allows developers to easily integrate existing protocols and build upon proven foundations.

Newer virtual machines offer technical advantages but face adoption hurdles. Many provide **better performance** through **parallel execution**, compiled code, and optimized architectures, alongside **stronger safety guarantees** with language-level protections against entire classes of bugs. These newer systems often provide **more expressive** programming environments with richer type systems and better abstraction capabilities that can lead to more maintainable code.

However, these technical improvements come with trade-offs in ecosystem maturity. Newer VMs typically suffer from **developer familiarity** gaps, with smaller pools of experienced developers compared to the **Solidity** community. **Tooling maturity** remains limited, with fewer debugging tools, testing frameworks, and **IDE integrations** available. The **audit expertise** for newer languages is scarce, creating potential security bottlenecks, while **ecosystem depth** remains shallow with fewer battle-tested libraries and protocols to build upon.

This creates a classic **innovator's dilemma** in blockchain development. Established technologies like the **EVM** benefit from **network effects** and ecosystem momentum, even when newer alternatives offer superior technical capabilities. For new virtual machines to achieve adoption, they must either provide significantly better **developer experience** that overcomes these ecosystem disadvantages, or target specific use cases that existing options serve poorly. Technical superiority alone is rarely sufficient to displace an entrenched ecosystem.

**Monad** exemplifies a pragmatic approach to this dilemma by choosing **EVM compatibility** while reimagining its execution model. Rather than creating an entirely new virtual machine, Monad maintains full **bytecode-level compatibility** with Ethereum, allowing existing **Solidity** contracts to deploy unchanged while targeting performance improvements through Monad's **parallel execution** engine that aims for **10,000 transactions per second**. 

This strategic decision preserves access to Ethereum's vast ecosystem - developers can use familiar tools like **Hardhat** and **Foundry**, auditors can apply their existing **Solidity** expertise, and protocols can port seamlessly - while the underlying architecture improvements deliver performance gains through **optimistic parallel execution**, **asynchronous I/O**, and a custom **database architecture**. By decoupling the developer-facing VM from the execution implementation, Monad demonstrates that chains can innovate on performance without sacrificing the **network effects** that make the EVM dominant.

## Section V: The Trilemma in Practice

### Understanding the Trade-offs

The **blockchain trilemma** is a practical design tension among decentralization, security, and scalability. It reflects real resource and coordination limits rather than a formal impossibility result. Balancing these three properties shapes every design decision in L1s, and understanding where different systems make these trade-offs reveals their sustainability and long-term viability.

**Decentralization** requires distributed infrastructure and coordination costs. Running validators across diverse geographic regions demands reliable networking, redundant systems, and operational expertise. Full node operation consumes significant resources: storage (often hundreds of GB depending on chain and pruning settings), bandwidth for propagating transactions and blocks, and computational power for validation. Decentralization also hinges on stake/hashrate distribution, network topology, MEV infrastructure (builders/relays), and home-validator accessibility. Client diversity materially reduces correlated-bug risk but isn't strictly required, though single-client monoculture creates known systemic risks.

**Security** derives from making attacks economically irrational. In PoS, security comes from staked value, rewards, and credible slashing; in PoW, from externalized costs (energy/hardware). In both, the effective security budget (issuance + fees, and in PoS also slashable stake) must make attacks uneconomic. Net dilution can be mitigated by fee burns or strong demand. The total security budget must exceed potential attack profits, creating a minimum viable economic threshold that smaller chains struggle to maintain.

**Scalability** improvements often shift costs elsewhere in the system. Throughput gains can pressure hardware requirements or shift complexity to L2s/bridges, introducing new risks. However, protocol techniques like sharding, data availability sampling, and validity proofs aim to scale while preserving permissionless participation. L2s change trust/latency/DA assumptions and add bridge risk, but wallets and account abstraction can hide most UX friction. Higher capacity tends to lower congestion fees per unit unless offset by demand growth, though total fee revenue can rise with increased usage.

### Hardware and Operational Requirements

The most visible trade-off appears in **validator hardware requirements**. Bitcoin nodes can run on modest hardware - a Raspberry Pi with sufficient storage can fully validate the chain. This enables broad participation but limits throughput to roughly **3-7 TPS depending on transaction size**.

**Ethereum** post-Merge requires more substantial hardware for validation but remains accessible to home operators. The **32 ETH minimum stake** and reasonable hardware requirements (**~32 GB RAM + 2-4 TB NVMe** recommended) maintain a **large, geographically distributed validator set (>1M active validators)** while supporting **~12-20 TPS in practice on L1** depending on gas usage and 12-second slots.

**Solana** demands high-end hardware: **high-clock CPUs, ≥12 cores/24 threads, ~256 GB+ RAM, fast NVMe, and ≥1 Gbps networking**. Validators commonly **prune ledger history by default** to manage storage requirements. This supports **thousands of TPS in normal conditions** with **theoretical ceilings ~50-65k TPS** (and recent stress-test peaks >100k), but concentrates validation among entities with significant resources due to higher operational complexity compared to Bitcoin/Ethereum.

The hardware spectrum creates a **decentralization gradient**. More demanding requirements improve performance but reduce the number of entities that can practically participate in consensus. This affects not just current participation but also barrier to entry for new validators.

### State Growth and Storage

**State Growth: The Hidden Scalability Killer**

While much attention focuses on transaction throughput, **state growth** poses an equally serious threat to blockchain scalability. State is the complete snapshot of all current data - every account balance, smart contract variable, and piece of stored information. Unlike transaction history which can be archived, state must remain immediately accessible for nodes to validate new transactions.

The problem is simple but severe: state only grows, never shrinks. Every new account created, every smart contract deployed, every piece of data stored adds to the state permanently. Even if an account becomes inactive or a contract is abandoned, its data remains in the state forever.

This creates compounding problems:

- **Hardware requirements spiral upward**: As state grows from gigabytes to terabytes, running a node requires increasingly expensive SSDs and RAM
- **Sync times become prohibitive**: New nodes must download and verify the entire state, taking days or weeks as state grows
- **Verification costs increase**: Every state access requires disk I/O, and larger states mean more cache misses and slower validation
- **Centralization pressure mounts**: When only data centers can afford to run nodes, the network loses its decentralized properties

Without intervention, state growth eventually prices out regular users from running nodes, undermining the fundamental value proposition of blockchains.

**Managing the State Explosion**

Fortunately, three main approaches have emerged to control state growth, each with distinct tradeoffs:

**State Rent** introduces ongoing storage fees - if you want to keep data on-chain, you must continuously pay for that privilege. This creates economic pressure to remove unnecessary state, similar to how cloud storage pricing encourages efficient data management. The challenge lies in implementation: suddenly charging rent for existing data could break thousands of applications that assumed permanent free storage.

**State Expiry** takes a more aggressive approach by automatically removing state that hasn't been accessed for a certain period (e.g., one year). If users need expired state later, they must provide cryptographic proofs of its previous existence. This hard cap on state size comes at the cost of significant complexity - applications must now handle the possibility that their data might disappear.

**Advanced Data Structures** like Verkle trees attack the problem from a different angle. Verkle trees are cryptographic structures that dramatically shrink the proofs needed to verify state data. Rather than reducing state size directly, they enable light clients - simplified nodes that don't store full state - to verify transactions using compact cryptographic witnesses. While promising, these structures require fundamental changes to how blockchains organize data.

**Combining Approaches**

Real-world implementations often combine multiple techniques. A rollup might implement state rent for economic efficiency while using Verkle trees to make witness generation practical. Or a blockchain might combine gentle state expiry - removing only provably lost accounts - with aggressive proof compression.

The key insight is that state growth isn't just about storage costs. It's about preserving the ability for ordinary users to verify the blockchain. Every solution involves tradeoffs between user experience, implementation complexity, and decentralization, making this one of blockchain's most nuanced scalability challenges.

### Client Diversity and Implementation Risk

**Client diversity** means having multiple independent implementations of the same protocol. Having multiple clients provides crucial protection against implementation bugs but adds coordination complexity. Ethereum maintains multiple consensus clients (Prysm, Lighthouse, Teku, Nimbus) and execution clients (Geth, Nethermind, Besu, Erigon).

When a single client implementation dominates, bugs in that client can affect the entire network. During the 2016 Shanghai DoS attacks, hackers exploited vulnerabilities in Geth, but Ethereum survived because nodes could switch to the unaffected Parity client - demonstrating how client monocultures create systemic risks.

The September 2025 Reth client bug offers a real-time example: while the bug completely halted nodes running affected versions, Ethereum's network remained stable because Reth represented around 5% of execution clients. This incident underscores both the protection that client diversity provides when present, and the systemic risk when a single client like Geth dominates with over 50% market share.

Maintaining client diversity requires significant ongoing investment. Each client team needs funding, coordination with other teams on protocol changes, and careful testing to ensure consensus compatibility. Smaller networks often struggle to fund multiple independent implementations.

### Economic Security Models

The relationship between **security budget** and actual security isn't straightforward. A chain spending $100 million annually on validator rewards doesn't necessarily provide $100 million worth of attack resistance.

**Proof-of-Work** security depends on the cost to acquire and operate sufficient hardware to reorganize the chain. This includes not just purchasing ASICs but also securing power, facilities, and operational expertise for a sustained attack period.

**Proof-of-Stake** security depends on the cost to acquire sufficient stake and the economic damage from slashing penalties. However, liquid staking derivatives, centralized exchanges, and lending markets can complicate these calculations by separating stake ownership from validation operation.

**Shared security** models like Cosmos Hub's replicated security or Ethereum's rollup model allow smaller applications to inherit security from larger validator sets. This can provide better security per dollar but creates new dependencies and trust assumptions.

The key insight: **security budget ≠ security guarantee**. The distribution of stake or hash power, the liquidity of attack resources, and the coordinated response capabilities of the community all affect actual security levels independent of raw spending amounts.

## Section VI: Scaling Patterns

### Vertical Scaling Approaches

**Bigger blocks** represent the most straightforward scaling approach - simply increase the amount of transaction data each block can contain. Bitcoin Cash chose this path with larger blocks (historically 32 MB; parameterization has evolved), while **BNB Smart Chain (BSC)** scales by tuning its *block gas limit* (currently ~140M gas). BSC's **2025 roadmap** proposes raising the block gas limit to **1 gigagas** (1,000,000,000 gas) - a 10× increase that's planned but not yet live. Exact throughput depends on block time and transaction mix. The trade-off is predictable: larger blocks require more bandwidth and storage, gradually excluding participants with limited resources.

**Shorter block times** can increase throughput without increasing per-block resource requirements. Ethereum's 12-second blocks process more transactions per minute than Bitcoin's 10-minute blocks, even with similar block sizes. However, shorter intervals increase uncle/orphan rates and may reduce security by giving attackers more opportunities to reorganize recent blocks.

**Pipelining and parallel execution** allow chains to process multiple aspects of block production simultaneously. While one set of validators executes transactions, another can propagate blocks, and a third can finalize consensus. Solana's Gulf Stream protocol pipelines transaction forwarding to expected leaders, reducing confirmation latency even before blocks are produced.

### Advanced Networking and Mempool Design

**Gossip networking** protocols determine how quickly transactions and blocks propagate through the network. Ethereum's execution layer uses devp2p while the consensus layer gossips via libp2p/GossipSub. (Compact block relay is a Bitcoin BIP-152 technique, not part of Ethereum's deployed stack.)

**QUIC and modern networking** protocols can significantly improve blockchain networking performance. QUIC provides built-in encryption, multiplexing, and connection migration - features particularly valuable for mobile validators or those with unstable network conditions.

**Leader scheduling** and **rotating proposers** create predictable patterns for block production. Solana's leader rotation allows validators to prepare transactions for their upcoming slots, while Ethereum's beacon chain randomly selects proposers to prevent MEV concentration.

## Section VII: Fees & Security Budget

Blockchain transaction pricing has evolved significantly beyond simple auction models, with each major Layer 1 developing distinct approaches tailored to their architecture. Bitcoin maintains a classic **first-price auction system** where miners collect fees directly, creating periodic congestion spikes. However, **Replace-by-Fee (RBF)** and **Child-Pays-for-Parent (CPFP)** mechanisms allow users to rebid stuck transactions, adding dynamic elements to the auction process. Ethereum introduced a more sophisticated **dual-fee system** post-EIP-1559, combining a protocol-set **base fee** that adjusts to target utilization (and gets burned) with priority tips, plus a separate **blob fee market** for Layer 2 data. Solana takes a different approach with **localized fee markets** using a fixed **base fee per signature** plus optional **priority fees per compute unit**, leveraging **parallel execution** to keep fees low under normal conditions but creating hotspots around **writable accounts and programs** that become congestion points.

The trend across newer networks like Aptos or Sui reflects a move toward more nuanced, multi-market fee designs. **Aptos** uses governance-set **minimum gas unit prices** with market-driven priority for inclusion speed, while **Sui** employs an **epoch-level reference price** determined by validator quotes, differentiating between **fast-path** owned-object transactions and **consensus-path** shared-object interactions. This evolution toward **localized or resource-specific fee markets** represents a broader industry shift away from one-size-fits-all pricing, instead aligning fees with specific bottlenecks and resource usage patterns to improve predictability and user experience.

However, two fundamental pressures now affect all blockchain ecosystems regardless of their fee design. First, **fee competition and modularity** create complex dynamics as execution migrates to L2s, sidechains, and subnets, potentially changing base layer revenue streams and raising questions about whether off-chain activity meaningfully contributes to **base-layer security**. Second, the increasing **liquidity of attack resources** (through hashrate rental markets, liquid staking, and centralized custodians) means that nominal security budgets don't necessarily reflect real attack costs. Ultimately, **practical security** depends not just on economic incentives but on factors like stake distribution, **client diversity**, credible slashing mechanisms, and coordinated response capabilities, making **realized security** distinct from theoretical security budgets.

## Section VIII: Governance & Upgrades

Blockchain governance fundamentally revolves around two approaches: **off-chain and on-chain mechanisms**. Bitcoin exemplifies the **off-chain model**, where protocol changes require broad consensus among developers, miners, and economic actors through years of discussion and testing, creating stability but slowing innovation. Ethereum uses a **hybrid approach** with off-chain governance for core protocol changes (via the EIP process and developer consensus) while enabling on-chain governance for application-layer decisions. The **DAO fork** demonstrated how **social consensus** can ultimately override pure technical considerations in critical situations.

Protocol foundations and core development teams wield significant influence despite decentralization ideals. Organizations like the Ethereum Foundation and Solana Foundation fund development and coordinate research while claiming to gradually reduce their control. Core development teams possess substantial de facto power through their technical expertise and contribution history. This creates tension between practical coordination needs and decentralization goals, with **developer capture** representing a key risk, though **forking rights** provide a crucial check on centralized power by allowing communities to migrate to alternative implementations.

**Client diversity** serves as a critical governance safeguard by preventing single implementation teams from unilaterally changing protocol behavior. Multiple client implementations create checks and balances, as seen in Ethereum's multi-client architecture, though they increase coordination complexity during upgrades. Historical incidents like Ethereum's 2016 DoS attacks and Bitcoin's 2010 value overflow bug (which briefly created 184 billion extra bitcoins before emergency rollback) highlight both the risks of implementation bugs and the importance of diverse implementations for rapid recovery.

Upgrade mechanisms have evolved to balance security, user autonomy, and deployment practicality. The 2017 SegWit activation demonstrated how **User Activated Soft Forks (UASF)** can enable economic actors to coordinate changes independently of miner preferences, with BIP-148 ultimately catalyzing miner adoption through BIP-91. Regional and regulatory considerations increasingly affect governance decisions, as validator geography and jurisdictional differences influence protocol evolution. Ultimately, the **social layer** (community culture, shared values, and informal decision-making processes) determines governance legitimacy regardless of formal mechanisms, often mattering more than specific voting systems or technical procedures.

## Section IX: Attention Game

**User adoption and product-market fit** have emerged as the scarcest resources in crypto, with dozens of prominent L1s (and potentially hundreds including smaller or forked chains) competing for a limited user base primarily consisting of crypto natives and retail speculators. Effectively no blockchain to date has achieved widespread sustainable demand for their applications outside of **trading** (decentralized exchanges), **speculation** (like NFTs or memecoins), **stablecoins**, **yield** (whether through lending or other strategies), and **payments/remittances** (particularly in emerging markets), though early pockets are emerging in areas like DePIN, and RWAs. A lot of the use cases that have gotten traction are due to both regulatory arbitrage and better efficiency that blockchains provide compared to archaic traditional banking rails (24/7 settlement, **faster cross-border transfers**, programmability, permissionless access, and global reach).

**Developer attention** is also crucial, networks deploy massive resources to attract and retain experienced talent through **grant programs** (collectively distributing hundreds of millions annually, with individual foundations like Ethereum typically spending ~$100–135M total annually including grants and research), hackathons, and accelerators. However, grants often fund experiments that never achieve sustainable adoption, and many hackathon projects remain prototypes. The most successful retention strategies focus on superior **developer tooling**: mature IDEs, testing frameworks, and documentation, which create compound effects that sustain growth long after initial financial incentives end, but ultimately must lead to applications with genuine user demand.

**Liquidity** serves as the ultimate kingmaker in determining network success, with **stablecoin distribution** playing a crucial role. Networks with native **USDC and USDT** support can tap into hundreds of billions in circulating stablecoins and trillions in annual transfer volume, while those without struggle to attract meaningful DeFi applications. **Central exchange listings** provide essential fiat on-ramps that determine practical user accessibility; superior technology means little if major exchanges don't support deposits and withdrawals. While **liquidity bootstrapping** through incentive tokens can jump-start activity, sustainable liquidity requires genuine user demand rather than temporary "**liquidity mining**" that evaporates when rewards end.

**Cultural and community dynamics** significantly impact long-term ecosystem sustainability beyond pure technical capabilities. Different networks cultivate distinct cultures: some emphasizing technical innovation, others prioritizing user experience or financial returns, which attract different participant types and shape development trajectories. **Regional specialization** is emerging, with networks gaining strength in specific geographic markets (like Binance Smart Chain in Asia or Ethereum in Western DeFi), creating self-reinforcing **geographic network effects**. Community governance mechanisms affect both decision-making quality and engagement levels, while **institutional adoption** patterns vary based on regulatory clarity and compliance features.

The competitive landscape demonstrates that **superior technology alone rarely guarantees ecosystem success**. Instead, complex interactions between technical capabilities, economic incentives, and social dynamics determine network outcomes. Networks must balance multiple factors simultaneously: attracting and retaining developers through effective tooling and support, securing crucial liquidity partnerships and exchange relationships, cultivating sustainable community cultures, and navigating regional and institutional adoption requirements. Understanding these **multifaceted network effects** is essential for evaluating the long-term prospects of different Layer 1 networks.

### Key Takeaways
Layer 1 blockchains bundle execution, settlement, consensus, and data availability, but differ in how they arrange and optimize these functions. Monolithic designs (e.g., Solana, Aptos/Sui) maximize local composability and performance at the cost of higher hardware and operational complexity, while modular designs (e.g., Ethereum with rollups and external DA) scale via specialization but introduce cross-layer composability and latency trade-offs. Consensus choices drive user trust and UX: PoW yields probabilistic finality, PoS targets faster economic finality, and BFT-style protocols provide deterministic finality with different liveness/safety balances.

Virtual machines and programming models shape both throughput and developer experience. The EVM’s tooling and ecosystem gravity enable rapid adoption across EVM chains, whereas SVM-style parallelism, Move’s resource safety, and WASM runtimes offer performance and safety advantages with steeper learning curves and thinner tooling. The trilemma shows up in practice through validator hardware requirements, decentralization gradients, state growth pressures, and the importance of client diversity; scaling techniques span bigger blocks, shorter block times, pipelining/parallelism, and better networking and mempool design.

Beyond pure tech, sustainable fees, MEV management, and security budgets, plus credible governance and upgrade processes, determine long-run resilience. Mindshare is won through liquidity (stablecoins, CEX integrations), developer attention (grants, hackathons, tooling), culture, and regional/institutional adoption.