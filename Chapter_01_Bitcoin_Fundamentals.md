# Chapter I: Bitcoin Fundamentals

## Section I: Bitcoin Core Concepts

### Genesis and Philosophy

Bitcoin's creation was a direct response to the 2008 global financial crisis. On January 3rd, 2009, its anonymous creator, Satoshi Nakamoto, embedded a newspaper headline into the very first block, known as the genesis block. The headline from *The Times*, "Chancellor on brink of second bailout for banks" serves as a permanent critique of a traditional financial system dependent on centralized control.

This act highlights Bitcoin's mission: to be an alternative to the traditional banking system. Its philosophy is rooted in the cypherpunk belief in using strong cryptography to achieve individual sovereignty over one's finances. To accomplish this, Bitcoin operates as a peer to peer electronic cash system without trusted third parties. Its monetary policy is predictable and enforced by code, featuring a fixed, immutable supply cap of 21 million BTC. This creates digital scarcity, standing in stark contrast to fiat currencies that central banks can print at will.

But creating a decentralized alternative to traditional banking raises a fundamental challenge: how do you get thousands of computers around the world to agree on who owns what, without a central authority to settle disputes?

### Consensus and Chain Selection 

Bitcoin solves this through a robust consensus mechanism. Bitcoin uses **Nakamoto Consensus**, which is often simplified as the "longest chain rule" but is more accurately described as the "heaviest chain rule." Nodes choose the valid chain with the greatest accumulated proof of work, computed from each block's target (nBits). Think of two hikers taking different routes: one logs 1,000 easy steps, the other 600 hard steps. We don't score by steps (block count) but by calories (a stand in for work) so the steeper, harder route can "weigh" more even with fewer steps. Likewise, nodes sum each block's work and follow the chain with the most total work. You can't win by making a long, low effort chain because difficulty rules are enforced; to rewrite history you must produce at least as much cumulative work as the honest chain (and more, if you're behind).

### Mining and Proof of Work

What if you needed to prove you'd done a lot of work, but couldn't trust anyone to verify it? Bitcoin solves this through **Proof of Work**, a system where miners compete to solve cryptographic puzzles that require enormous computational effort but can be quickly verified by anyone.

Here's how it works: Miners bundle transactions into a block and repeatedly hash the block header using the double SHA 256 algorithm. They're searching for a hash value below a specific target, like rolling dice until you get a number lower than a certain threshold, except they're "rolling" trillions of times per second.

**Hash rate** is the speed of this guessing process: how many hashes a miner or the entire network can try each second while searching for a valid block. More hash rate means more chances per second to find a block. It's measured in hashes per second (H/s), commonly shown as TH/s (terahashes), PH/s (petahashes), or EH/s (exahashes). Importantly, higher total network hash rate doesn't make blocks come faster on average; difficulty adjusts to maintain the ~10 minute target.

To generate different guesses, miners vary several fields: the **nonce** (a 32 bit number offering about 4 billion attempts), the timestamp, and sometimes the version field. When the nonce space is exhausted, miners modify arbitrary data in the coinbase transaction (often called an **extra nonce**) which changes the block's Merkle root and effectively gives them a fresh header space to search.

To keep the average block time at approximately 10 minutes, the network performs a **difficulty retarget** every 2,016 blocks (about two weeks). The algorithm measures the actual time taken for those 2,016 blocks and adjusts difficulty accordingly, though it clamps extreme changes between ¼× and 4× to prevent wild swings.

Hash rate comes from **ASIC hardware**, specialized computer chips designed solely for Bitcoin mining that are thousands of times more efficient than regular computers. These ASICs are typically organized into mining pools, where thousands of miners combine their computing power and share rewards proportionally. Pools coordinate this work using the **Stratum protocol**, which gives each miner a unique coinbase and job template so everyone searches distinct header space while avoiding duplicate work.

Miners use pools because finding a block is like a huge lottery. With one home ASIC, your chance on any given day is tiny - you could wait years and still never hit one. Pools let miners combine their hash rate so blocks are found regularly, and rewards are split by each miner's share of work. That means steadier, more predictable payouts instead of long dry spells.

Occasionally, two miners find valid blocks at nearly the same time, creating temporary forks in the blockchain. These **stale blocks** and brief **chain reorganizations** are normal; the network automatically settles on the chain with more accumulated work. This is why merchants typically wait for multiple **confirmations** (additional blocks built on top) before considering large payments final.

### Monetary Policy

Bitcoin has a predictable, algorithmic monetary policy with a fixed issuance schedule. The **block reward**, or subsidy, is cut in half every 210,000 blocks, an event known as the **"halving"** that occurs roughly every four years. The subsidy began at 50 BTC and has since been reduced to 25, 12.5, 6.25, and most recently to 3.125 BTC after the 2024 halving.

This mechanism makes Bitcoin a **disinflationary asset**, as its inflation rate trends toward zero. Around the year 2140, the subsidy will cease, and miners will be compensated solely by transaction fees. Due to integer rounding in halvings, the terminal supply converges to ~20,999,999.9769 BTC.

The miner **security budget** (total revenue paid to block producers from subsidy plus fees) presents both current stability and future challenges. While this budget is straightforward to calculate in BTC terms, the relevant metric for gauging attack resistance is **USD per unit time**, since both miners and potential attackers procure hardware, facilities, and energy in fiat terms. As specialized hardware improves and the cost per hash declines, what matters economically is the dollar cost to acquire and operate enough hash rate for long enough to reliably reorganize the chain.

This framing reveals a critical long term concern: if transaction fees and BTC price do not rise sufficiently to offset successive halvings, the USD denominated security budget will trend lower. A materially smaller budget can lead to miner exits, weaker competition for blocks, and reduced costs for would be attackers to acquire majority hash rate. As the subsidy approaches zero around 2140, durable **fee demand** must carry the entire security budget through payments, L2 settlements, inscriptions, batched rollup data, and other valuable uses of block space.

Bitcoin's predictable scarcity forms a cornerstone of its store of value proposition, though this mechanical constraint must be paired with sustained adoption and usage to drive long term value accrual.

## Section II: Bitcoin Technical Architecture

### UTXO Model

How do you track ownership in a system without accounts? Bitcoin takes a different approach from traditional banking by using an **Unspent Transaction Output (UTXO) model**.

Think of it like physical cash in your wallet. Instead of having a single account balance, you have individual bills of different denominations: a $20, two $5s, and some $1s. When you buy something for $7, you might use a $5 and two $1s, getting back change if needed.

Bitcoin works similarly. Instead of a single balance, your wallet holds a collection of UTXOs (individual digital "coins" of varying amounts). When you send bitcoin, your wallet performs **coin selection** (choosing which UTXOs to spend, with privacy and fee trade offs), consumes them entirely, and creates new UTXOs as outputs: one for the recipient and another as "change" back to you. This elegant design prevents double spending: once a UTXO is spent in a confirmed transaction, it's permanently removed from the UTXO set and can never be spent again.

Each full node maintains its own view of the global **UTXO set** (the complete collection of all spendable outputs) derived from the validated blockchain.

**Bitcoin Script** is a simple programming language that defines spending conditions. Each output carries a **locking script** (scriptPubKey), and inputs provide **unlocking data** (scriptSig and/or witness for SegWit) that must satisfy that script. Addresses are just encodings of common script templates like P2PKH, P2SH, P2WPKH, and P2TR (Taproot).

**Timelocks** make transactions invalid until a specified time or block height, either **absolute** timelocks (nLockTime or OP_CHECKLOCKTIMEVERIFY) or **relative** timelocks (nSequence with OP_CHECKSEQUENCEVERIFY). These enable more complex contracts like Lightning channels, vaults, and escrow arrangements.

### Transaction Structure and Prioritization

Once you understand how UTXOs work, the next question is: how do transactions actually get processed? A Bitcoin transaction consists of **inputs** (the UTXOs being spent) and **outputs** (the new UTXOs being created). The transaction **fee** equals the sum of inputs minus the sum of outputs. Once broadcast, transactions enter each node's **mempool** (a pool of unconfirmed transactions).

Here's where economics comes into play. Since blocks are limited to 4,000,000 weight units (~1,000,000 vB), miners must choose which transactions to include from their own mempools. They naturally prioritize transactions that pay the highest **fee rate**, measured in satoshis per virtual byte (sats/vB), where virtual bytes are derived from transaction weight. A satoshi is the smallest unit of bitcoin; there are 100 million satoshis in one bitcoin.

This creates a **fee market** where users essentially bid for block space. Need your transaction confirmed quickly during network congestion? Pay a higher fee rate. Can wait? Pay less and wait for a quieter period. If your transaction gets stuck, you can use **Replace by Fee (RBF)** to broadcast a higher fee replacement, or **Child Pays for Parent (CPFP)** to create a high fee child transaction that incentivizes miners to include the parent. Use CPFP when you can't (or don't want to) replace the parent but control one of its outputs (sender's change or the recipient's output). Use RBF when you control the original tx and it can be replaced.

---

## Section III: Bitcoin Upgrades and Scaling

### Bitcoin Core: The Reference Implementation

**Bitcoin Core** is the predominant implementation of the Bitcoin protocol and the de facto standard most nodes use. It doesn't *control* Bitcoin or unilaterally define the rules, but because there's no formal spec, Core's consensus code effectively serves as the common reference most of the economy follows. Originally developed by Satoshi Nakamoto and now maintained by a global community of developers, Bitcoin Core is the software that most Bitcoin nodes run to participate in the network.

Proposals for changes are documented as **BIPs** (Bitcoin Improvement Proposals); when adopted, Core typically ships the implementation. Most releases adjust **policy** (mempool/relay) defaults, while **consensus** changes are rare and only take effect through soft fork activation mechanisms (e.g., BIP9 or Speedy Trial). For example, recent versions have focused on mempool policy improvements rather than consensus rule changes.

In practice, Bitcoin Core's careful development process, extensive testing, and broad adoption make it the standard that other implementations follow. Major upgrades such as SegWit and Taproot were implemented in Core and activated by the network through specific soft fork mechanisms, demonstrating how protocol evolution works through this reference implementation.

As a concrete example of a policy (not consensus) change: the historical ~80 byte relay cap on **OP_RETURN** outputs is slated to be removed by default in Bitcoin Core v30. This doesn't change what's valid on chain; it changes default relay/mempool behavior, and operators can still run stricter policies. The takeaway is that many Core releases adjust node policy rather than consensus rules.

### Understanding Fork Types

How do you upgrade a decentralized network where no one's in charge? Bitcoin has two main upgrade mechanisms that allow the protocol to evolve while maintaining consensus.

#### Hard Forks

**Hard forks** are incompatible upgrades that loosen or change consensus rules. Think of it like changing the width of train tracks. If your train (node) doesn't switch to the new wheel size, it simply can't run on the new tracks. Everyone has to upgrade or they'll keep running on the old line, which becomes a different railway. Bitcoin avoids this because coordinating a whole railway swap is risky and can split passengers and schedules for good. Hard forks are extremely rare in Bitcoin due to coordination challenges and the risk of permanent network splits. 

A notable example is Bitcoin Cash (BCH), created in 2017 by changing rules (notably much larger blocks). In practice, that approach fractured liquidity and community mindshare; over time BCH has retained only a small fraction of Bitcoin's adoption, hashpower, and market value. Critically, though, deciding what's the "real Bitcoin" isn't something the code can decree; there's no central authority. It's a messy blend of social consensus (what users, exchanges, wallets, and merchants run), economic gravity (where liquidity settles), and security assumptions (what most full nodes enforce). Markets have decidedly treated BTC as the Schelling point, but that outcome is ultimately social, not ordained.

#### Soft Forks

**Soft forks** are backward compatible protocol upgrades that tighten consensus rules without breaking the network. Think of it like a club tightening its dress code from "no beachwear" to "collared shirts only." People who didn't hear about the new rule can still walk in and think everything's fine, because the club still looks and works the same to them. The upgraded bouncers enforce the stricter rule; the non upgraded ones don't, but they still recognize everyone as legitimate club members. Non upgraded Bitcoin nodes still see new blocks as valid but don't enforce the stricter rules themselves, allowing the network to upgrade without splitting into incompatible versions. They require majority support to avoid chain splits, with examples including SegWit, Taproot, and the disabling of OP_CAT.

#### Activation Mechanisms

**Miner Activated Soft Forks (MASF)** rely on hash power signaling; miners indicate readiness by including version bits in block headers. Once a threshold (typically 95%) is reached, the soft fork activates. This was used for upgrades like SegWit (eventually) and most historical soft forks.

**User Activated Soft Forks (UASF)** represent an alternative where economic nodes coordinate a "flag day" to start enforcing tighter rules, potentially regardless of miner signaling. If enough economic nodes and service providers participate, miners face a simple incentive: follow the new rules to get paid, or mine a chain most users won't accept.

**Speedy Trial** is a short BIP9 style miner signaling trial with a **90%** threshold over 2,016 block windows. If it locks in, activation occurs later at a preset block height; if it times out, no activation occurs and other mechanisms can be considered. This method was successfully used for Taproot activation in 2021.

#### The Challenge of Change

Despite backward compatibility, getting any soft fork into Bitcoin is intentionally difficult. Many developers prioritize **protocol ossification** (the idea that Bitcoin should become increasingly resistant to change as it matures). This conservative approach means proposals undergo years of review, testing, and community debate.

### Bitcoin's Major Upgrades

#### Early Soft Forks (2010 to 2012)

Bitcoin's earliest soft forks focused on security improvements. The **OP_CAT removal in 2010** disabled the OP_CAT opcode to prevent potential denial of service attacks. Various other opcode restrictions were implemented during this period to tighten script validation and improve overall security.

#### Segregated Witness - SegWit (2017)

The **SegWit activation saga** represents one of the most important case studies in Bitcoin's governance, demonstrating how protocol upgrades work (and sometimes don't work) in a truly decentralized system.

SegWit was a landmark upgrade that solved multiple critical issues. Before SegWit, Bitcoin had a critical bug: third parties could alter a transaction's signature and change its ID (TXID) before confirmation, without affecting the transaction's validity. This **transaction malleability** made it risky to build dependent transactions or second layer protocols like Lightning.

SegWit moved signature data to a separate "witness" structure, making transaction IDs immutable once created. It also introduced **block weight** (a new measurement system with a 4,000,000 weight unit maximum instead of a simple 1MB limit). This effectively increased block capacity while incentivizing adoption of more efficient SegWit addresses. The weight system counts witness data as one quarter for weight calculation (commonly described as a "75% discount"), creating a backwards compatible blocksize increase.

To understand the political dynamics, it's helpful to think of pre SegWit Bitcoin as **"Bitcoin 1.0"** (a system with a hard 1MB blocksize limit and transaction malleability issues). **SegWit represented "Bitcoin 1.1"** (mostly backwards compatible with Bitcoin 1.0, but fixing protocol bugs and enabling second layer networks while providing a one time capacity increase).

The original activation mechanism used BIP 9 with a 95% threshold: during any 2,016 block difficulty adjustment period within the window from November 15, 2016 to November 15, 2017 (UTC), if 95% or more of mined blocks signaled SegWit readiness, the upgrade would lock in. After a grace period, SegWit would activate and the network would accept the new transaction types.

However, some large miners withheld signaling, treating "SegWit Readiness" signaling as a "SegWit Willingness" indicator instead. Despite years of development work by Core developers and third party services, and support from many economic nodes, these miners were blocking activation by refusing to signal (not because of technical concerns, but as political leverage in the broader "blocksize wars").

This created an unprecedented situation: many participants in the Bitcoin ecosystem supported an upgrade they believed would benefit the network, but a group of miners could indefinitely block progress through coordinated non signaling.

**BIP 148** represented a proposed solution to this governance deadlock. BIP 148 **changed consensus rules for participating nodes by rejecting any non signaling (bit 1) blocks after August 1st, 2017**. While it leveraged the existing BIP 141 deployment, this "reject non signaling blocks" rule was new and could have caused a chain split if not widely adopted.

The mechanism was straightforward: **BIP 148 nodes would reject any block that failed to signal SegWit support after the flag day**. This created economic pressure by making non signaling blocks invalid for BIP 148 nodes, potentially forcing miners to choose between signaling support or mining a chain that some economic actors would reject.

If enough economic nodes (exchanges, services, businesses) ran BIP 148, miners faced a stark choice: signal SegWit support and get paid in bitcoin that the broader economy would accept, or mine a chain that major economic actors would ignore.

The threat of BIP 148 created powerful economic incentives that ultimately resolved the impasse:

- **BIP 91**: Locked in July 21, 2017 → Activated July 23, 2017 (enforced that miners signal bit 1, enabling BIP 141 to reach its threshold)
- **BIP 148 (UASF)**: Planned August 1, 2017 flag day to reject non SegWit signaling blocks
- **SegWit (BIP 141)**: Locked in August 9, 2017 → Activated August 24, 2017 (block 481,824)

Faced with the credible threat that many economic nodes would enforce SegWit activation regardless of miner preferences, the miners began signaling support. BIP 91 was deployed as an intermediate solution that allowed miners to signal SegWit support before the August 1st UASF deadline.

The SegWit activation demonstrates several crucial principles:

1. **Economic nodes can influence protocol rules** when there's sufficient coordination. Miners must produce blocks that the economic majority will accept and value.
2. **Soft forks can be enforced by users** when there's sufficient economic coordination, even against miner resistance.
3. **Credible threats matter more than actual deployment**. BIP 148 succeeded largely because the threat was believable, not because a majority of nodes actually ran it.
4. **Bitcoin's governance is antifragile**. The system found a way to route around the blockade and activate beneficial upgrades despite coordinated resistance.

While SegWit technically activated via the original miner signaling mechanism (BIP 141), the credible UASF threat (BIP 148) was a significant catalyst that helped resolve the impasse. This demonstrated that Bitcoin users and economic nodes can coordinate to influence protocol governance, even when facing miner resistance.

#### Taproot (2021)

The **Taproot upgrade** significantly improved programmability and confidentiality. Taproot locked in June 2021 and activated in November 2021. **Schnorr Signatures** enable key and signature aggregation through schemes like MuSig2, allowing complex multi party transactions to appear as single signatures on chain. **Merkleized Abstract Syntax Trees (MAST)** structure complex spending conditions efficiently, where only the condition that's met needs to be revealed.

Together, these features provide major benefits: complex transactions become indistinguishable from simple payments for key path spends, delivering significant privacy and scalability improvements. When script path spends are used, only the revealed branch is disclosed, maintaining privacy for unused conditions.

### Address Types and Formats

Bitcoin addresses have evolved to improve efficiency and enable new features: Legacy (starts with 1) is the oldest and works everywhere but typically incurs slightly higher fees; P2SH (starts with 3) is a broad compatibility wrapper often used for multisig or older SegWit, and addresses starting with 3 are not necessarily multisig; Native SegWit (starts with bc1q) is the modern default with lower fees and all lowercase safety; and Taproot (starts with bc1p) is the newest, enabling advanced features with good fee efficiency and broad support across modern wallets (some services are still catching up). To avoid any confusion, address is not the same thing as a public key; it's an encoding (often a hash) of a public key or script (Taproot uses the key directly).

---

## Section IV: Bitcoin Layer 2 and Extensions

### Lightning Network

The **Lightning Network** attempts to enable faster Bitcoin payments through a Layer 2 protocol that moves small (sub $20) day to day payments off the main blockchain. Rather than broadcasting every payment to the entire network, two parties can open a private **payment channel** by locking funds in a shared on chain account (technically a **2 of 2 multisig output**). Once established, both parties can transact by updating their channel's balance sheet off chain, with all state changes requiring mutual agreement and secured by cryptography.

The network can theoretically route payments across multiple interconnected channels using **HTLCs** (Hash Time Locked Contracts) and **onion routing** for privacy, while **watchtowers** monitor for cheating attempts. However, Lightning faces significant **liquidity constraints** that limit its practical utility. Users need **outbound liquidity** to send payments and **inbound liquidity** to receive them. When channels lack sufficient liquidity, it results in **payment failures** or forces users to split larger payments across multiple routes.

Think of Lightning as a canal system with locks; you can only send if there's enough water on your side (outbound capacity) and only receive if the other side has room (inbound capacity). **Channel rebalancing** helps redistribute liquidity but incurs fees and takes time. Multi hop routes only work when each channel along the path has liquidity flowing the right direction.

This approach addresses Bitcoin's base layer limitations for small payments. Bitcoin is optimized for **high assurance settlement**, making "coffee payments" economically inefficient due to high fees and block space constraints. Lightning attempts to shift low value, high frequency activity off chain while preserving the option to settle back to Layer 1 when needed.

**Adoption challenges** have proven substantial. **Merchant adoption** faces challenges from integration complexities and Bitcoin's price volatility, though major exchanges like Coinbase and Kraken now support Lightning with notable transaction volumes. **User experience** barriers persist, as managing Lightning channels is complex for non technical users. Users must **pre deploy liquidity** in channels and navigate the separation between Layer 1 and Layer 2, adding operational complexity.

Higher base layer fees create additional stress by increasing **channel opening and closing costs**. While fee spikes can endanger on chain enforcement, the ecosystem has developed solutions like **anchor outputs** and **package relay** rather than simply requiring longer timelocks. Fee spikes can trigger **forced expiration scenarios** when many channels must settle on chain simultaneously.

---

## Section V: Bitcoin Network Operations and Security Model

**Roles at a Glance**

The Bitcoin network operates through distinct but interconnected roles that each serve essential functions. **Users and wallets** create and sign transactions before broadcasting them to the network, and importantly, they can do this without running their own node.

**Full nodes** independently validate and relay both transactions and blocks while enforcing **consensus rules** for themselves, though running a node is distinctly different from **mining**. **Miners** take on the energy intensive role of assembling validated transactions into candidate blocks and performing **Proof of Work** to compete for block production rights. Most miners run full nodes, but their core job is **block creation**.

Miners wield significant but limited influence within the Bitcoin ecosystem. They control **transaction inclusion and ordering** decisions, determine which **valid fork** they choose to mine on, and possess the ability to create short-term **reorganizations** and implement **censorship** within the existing rules. However, their power has clear boundaries. Miners cannot control the **validity rules** themselves, as **full nodes enforce these rules** regardless of **hash rate**. They cannot make invalid blocks or rule changes "valid" without gaining consent from the nodes that verify transactions and the broader **market** that values the coin. Any attempt to override these constraints simply creates a **different chain** that users can choose to ignore.

The **market** ultimately determines what constitutes "Bitcoin" through the collective choices of users, exchanges, custodians, merchants, and wallets regarding which coin they value and transact with. Since miners receive payment in that coin, they face strong **economic incentives** to mine the chain that these key actors accept and support. This influence operates through **social and economic mechanisms** rather than formal protocol roles. Users still require some aligned **hash rate** to ensure **liveness and security** under their chosen rules, though coordinating a true **"economic majority"** remains challenging in practice.

**Full nodes** form the network's backbone by storing the complete **blockchain** and independently **validating** all transactions and blocks against **consensus rules**. **Pruned nodes** provide the same validation security as full nodes but conserve disk space by discarding old block data after verification. **SPV (Simplified Payment Verification) clients**, which are commonly found in mobile wallets, take a lighter approach by downloading only **block headers** and relying on full nodes for transaction validation.

To find each other, the network maintains its **decentralized topology** through **peer to peer discovery** mechanisms, primarily using **DNS seeds** and direct peer to peer exchange to help nodes find and connect with other participants in the network.

### Block Propagation and Network Synchronization

When a new node joins, it performs an **Initial Block Download (IBD)** to sync the entire blockchain from its peers. To ensure new blocks propagate quickly and efficiently, the network uses optimized protocols like **Compact Block Relay**, which minimizes bandwidth by only sending information that nodes don't already have. Nodes also engage in **mempool synchronization** to share unconfirmed transactions. The network is resilient to partitions (temporary splits), which self heal once connectivity is restored. The network also uses additional protocols like **FIBRE** (fast relay) and **Erlay** (proposed mempool gossip reduction) to improve propagation latency and bandwidth efficiency.

### Attack Vectors and Economic Security

Bitcoin's security depends on making attacks too expensive to be profitable. The most cited threat is a **51% attack**, where an entity controlling a majority of the network's hashpower could attempt to rewrite history. However, the immense cost of acquiring and running this hardware, combined with the fact that a successful attack would devalue the asset, makes it economically irrational.

Security is achieved through **confirmation depth**; each subsequent block exponentially increases the work required to alter a transaction. This leads to **probabilistic finality**, where after a certain number of confirmations (e.g., six), a transaction is considered irreversible. The system is designed so that economic incentives strongly reward miners for honest behavior.

Bitcoin is designed to be **antifragile**; it grows stronger from stress and attacks. Its resilience stems from several factors: geographic distribution of nodes and miners resists localized disruptions, **protocol ossification** or resistance to change enhances stability and predictability, and its design assumes an adversarial environment, built to function despite malicious actors. The network has survived numerous technical, political, and economic challenges, demonstrating its robust and self healing nature.

#### Chain Reorganizations (Reorgs)

Chain reorganizations are a normal and expected part of Bitcoin's operation. When two miners find valid blocks around the same time, the network can briefly have competing tips. Nodes follow the chain with the most accumulated work; blocks on the losing tip become stale. One block reorgs occur occasionally; two block reorgs are rare; three or more are extremely rare absent an attack or severe network partition. This probabilistic behavior is why confirmations matter: the probability that a transaction is affected by a reorg falls exponentially with each additional block.

Other threats include **eclipse attacks** (peer isolation, where an attacker monopolizes a node's peers to feed it a distorted view of the network) and **selfish mining** (withholding found blocks to mine privately and publish strategically for a revenue advantage); diversity of peers, network level protections, and monitoring help mitigate these risks.

### Privacy Model

How private are Bitcoin transactions? Bitcoin is **pseudonymous**, not anonymous. While addresses are not directly linked to real world identity, transaction graph analysis can be used to cluster addresses and track the flow of funds. This risk is significantly increased by address reuse. Furthermore, **KYC/AML** regulations at crypto exchanges create links between on chain activity and real world identity, creating privacy gaps. Companies like Chainalysis have built billion dollar businesses on de anonymizing blockchains.

Common privacy practices include avoiding address reuse and optionally leveraging **CoinJoin style tools** to reduce heuristic linking. CoinJoin combines inputs from many users into a single transaction that produces many outputs of identical (or near identical) denominations. Because all inputs sign the same transaction, on chain observers cannot reliably determine which input funded which output. This breaks common heuristics like "multi inputs belong to the same owner" and "change output detection," creating an anonymity set where each coin could plausibly belong to any participant. Modern implementations add features like input registration over Tor, output blinding, equal output denominations, and multi round mixing to further resist clustering and improve plausible deniability.

---

## Section VI: Bitcoin Ordinals

### Ordinal Theory 

**Ordinal theory** assigns every individual **satoshi** a unique serial number that allows it to be tracked as a distinct unit of bitcoin as it moves through transactions. This numbering system enables users to attach arbitrary data to specific satoshis, creating what are known as **inscriptions** - turning individual sats into carriers of digital content.

The technical implementation of inscriptions follows a **two step process** called "commit → reveal." First, a **commit transaction** creates a Taproot output that commits to the inscription script. Then, a **reveal transaction** spends that output and discloses the actual bytes of the inscription. The data itself lives in the **taproot script path witness** of a Bitcoin transaction, using SegWit and Taproot's witness space to store content directly on chain. This design makes Ordinals different from schemes like **Bitcoin STAMPS**, which embed data in UTXOs to resist pruning. Ordinals prioritize **on chain provenance** with flexibility and lower overhead. Archival and indexer nodes retain inscription media, while pruned nodes may delete older witness data after validating it.

### Bitcoin-Native NFTs

An **inscribed sat** functions like a Bitcoin native NFT (a unique token with on chain content and provenance that transfers by moving a specific unit). The architectural difference from Ethereum's NFTs is notable: while Ethereum relies on **smart contract standards** like ERC 721/1155 with often off chain media storage, Bitcoin achieves uniqueness through **ordinal numbering** of sats, with media bytes embedded directly in the blockchain's witness data. The result is an NFT like **digital artifact** whose rules are enforced by Bitcoin's transaction model combined with **off chain indexers** that follow Ordinal conventions.

Transferring an inscription requires **sat control** (careful coin selection to ensure the input and output ordering moves the target sat and not surrounding ones). Purpose built wallets and the reference **`ord` tooling** provide this precise sat selection capability. Many practitioners recommend keeping inscribed sats in separate **Taproot addresses** to avoid accidental merges or spends, while marketplaces often use **PSBTs** (Partially Signed Bitcoin Transactions) so users can verify exactly which inscription is being transferred before signing.

### BRC-20: Experimental Fungible Tokens

**BRC-20** is an experimental convention for fungible tokens on Bitcoin that uses Ordinal inscriptions. Rather than relying on smart contracts, BRC-20 uses small **JSON inscriptions** that describe three fundamental actions: **deploy**, **mint**, and **transfer**. Community **indexers** reconstruct balances by reading the ordered history of these inscriptions, creating a system of "rules by convention" rather than enforcement by Bitcoin Script.

The BRC 20 system works through specific inscription types: a **deploy inscription** initializes a ticker (typically four letters) and parameters like maximum supply and optional decimals; **mint inscriptions** credit balances to the first owner of each mint inscription (not the deployer unless they own the mint); and **transfer inscriptions** earmark amounts to send. This framework operates as a **consensus by indexers** model, where validity and ordering depend on community agreement rather than cryptographic enforcement.

### The Transfer Process

A **BRC 20 transfer** follows a two step process layered over Bitcoin's UTXO model. First, users must inscribe a JSON object declaring their intent to transfer a specific number of tokens, receiving this **transfer inscription** in the same wallet that holds their BRC 20 balance. This step moves tokens from an "**available**" balance to a "**transferable**" pool in the eyes of indexers. Second, the transfer inscription itself must be sent to the recipient's address; when that transaction confirms, indexers debit the sender's balance and credit the recipient.

This process creates a distinction in user experience: sending a single **inscribed artifact** resembles moving a unique object; you select the exact UTXO containing that specific sat and deliver it. **BRC 20 transfers** operate more like managing ledger entries with a paper trail: you create a signed note (the transfer inscription) that locks an amount for sending, then send that note to the recipient. Both approaches require normal Bitcoin fees and **Taproot compatible addresses**, but their bookkeeping mechanisms differ.

### Strengths and Limitations

Ordinals provide a path to **digital artifacts** on Bitcoin without requiring new opcodes or smart contracts, using the existing capabilities of Taproot and SegWit's witness space. This simplicity means that certain behaviors - such as **collection-wide rules**, **royalties**, or **token supply enforcement** - exist outside Bitcoin Script and depend on indexers and community conventions.

**BRC 20** extends the Ordinal concept to fungible tokens while remaining explicitly experimental. Even its original creator points to alternative asset systems as more purpose built solutions. Both Ordinals and BRC 20 work across multiple wallets and marketplaces today, but they're best understood as **conventions anchored to real Bitcoin transactions** rather than contract enforced protocols.

To understand this ecosystem: imagine Bitcoin as a railway where every satoshi represents a seat, and every transaction moves seats between carriages. **Ordinal inscriptions** are like attaching small artworks to specific seats; wherever that seat travels, the artwork goes with it, and you must control that exact seat to transfer the artwork. **BRC 20** operates like a ticketing system built on the railway's record keeping: people leave signed notes declaring "move 100 units from me to Alice," and clerks monitoring the system (**indexers**) adjust everyone's balances when they observe the note traveling from sender to recipient.

The trains, tracks, and carriages remain standard Bitcoin infrastructure; the artworks and ticketing systems represent conventions layered on top. This architecture demonstrates how Bitcoin's base layer can support digital asset systems through creative use of existing features, enabling new use cases while maintaining the network's fundamental properties.