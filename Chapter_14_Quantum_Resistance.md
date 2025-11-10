# Chapter XIV: Quantum Resistance

## Section I: Quantum Computing

### How Quantum Computers Are Different

Think of regular computers like a light switch: it's either on (1) or off (0). Every calculation happens by flipping millions of these tiny switches very quickly, but they can only be in one state at a time.

Quantum computers are like special light switches that can be both on AND off at the same time. Even stranger, these switches can be entangled, showing strong correlations even over long distances (though this doesn't allow faster-than-light messaging).

This means these systems can explore many possible solutions simultaneously instead of checking them one by one. Imagine trying to escape a maze. A regular computer would try each path one at a time, while a quantum processor could explore all paths at once. The real trick is interference effects, which amplify the good paths and cancel out the bad ones to find the exit faster.

However, these machines don't make everything faster. They only provide major advantages for certain specific types of problems, like breaking codes and searching through unsorted information with a quadratic speedup.

#### The Encryption Challenge

Today's encryption is like an incredibly complex padlock that would take regular computers billions of years to pick. We rely on math problems that are easy to verify but practically impossible to solve backwards.

For example, it's easy to multiply two huge numbers together, but extremely difficult to take that final number and figure out what the original two numbers were. This is the foundation of most internet security today.

Quantum computers could potentially solve these "impossible" math problems much faster, which means we need entirely new types of digital locks.

However, the quantum threat isn't uniformly devastating across all cryptographic systems. Public key encryption systems like RSA and ECC, which are the kind used when users first connect to a website, are most at risk. A quantum algorithm called **Shor's algorithm** can break them on a sufficiently powerful machine. 

However, symmetric encryption, which is used for the actual data transfer, isn't broken by these systems. We may just need larger symmetric keys like AES-256 for long-term data protection. Hash functions remain viable too, using longer hash outputs like SHA-256 or SHA-384 preserves security against quantum attacks.

#### What's At Stake

Today's digital world runs on encrypted communication in ways most people never think about. Every time someone checks their bank balance, sends a private message, makes an online purchase, or logs into their email, encryption protects that information.

Beyond personal data, encryption secures power grids, air traffic control systems, military communications, and the backbone of the internet itself. It enables secure voting systems, protects journalists' sources, and allows people to communicate safely under oppressive governments.

The "https" padlock in browsers, the security updates on phones, and even the chip in credit cards all depend on encryption that these machines could theoretically break.

#### The Timeline Problem

One of the trickiest aspects is that we don't know exactly when quantum computers will become powerful enough to break current encryption. In October 2025, Google announced a significant milestone with their algorithm called "quantum echoes." The system successfully computed molecular structures in ways that classical supercomputers cannot, demonstrating what experts call "quantum advantage."

However, current systems can't threaten encryption. Google's breakthrough computed a narrow scientific problem, but breaking modern cryptography would require machines with hundreds of thousands to millions of stable qubits. Today's systems struggle to maintain even smaller numbers in the extremely controlled conditions they need.

The timeline remains uncertain. Google estimates real-world applications remain about five years away, while cryptanalytically relevant systems capable of breaking encryption will take considerably longer.

To put this in perspective, these cryptanalytically relevant quantum computers would need specific capabilities to crack encryption. Early estimates suggested it would take about 20 million quantum bits (called "qubits") and 8 hours to crack RSA-2048 encryption. Recent work by Gidney (2025) brings this estimate down to fewer than 1 million qubits and less than a week. These estimates assume nearly perfect quantum computers with almost no errors, something today's quantum computers are nowhere near achieving.

Realistically, we're looking at the early 2030s at the absolute earliest. More likely, it'll be sometime between the mid-2030s and 2040s. It could even take longer if engineers hit unexpected roadblocks or faster if breakthroughs happen quicker because of unforeseen AI progress.

There's also a "steal now, decrypt later" risk where bad actors could be collecting encrypted data today, planning to crack it once powerful quantum computers become available. This makes protecting long-term secrets especially important.

It's like knowing a big storm is coming but not sure if it's next week or next decade. The smart approach is to start preparing now rather than wait and see.

#### The Cryptographic Solution

Cryptographers have been preparing for this "quantum transition" for over a decade. In 2024, the U.S. government approved the first set of new encryption standards designed to resist quantum computers. Think of it like upgrading from mechanical locks to smart locks throughout an entire city. It's a big project, but manageable with proper planning.

This effort is part of a global, coordinated response led by organizations like the U.S. **National Institute of Standards and Technology (NIST)**. For over half a decade, NIST has been running a public competition to vet and select a portfolio of quantum-resistant cryptographic algorithms. The first set of these standards was finalized in 2024, providing a trusted foundation for the industry's transition.

These new standards include algorithms from different mathematical families, primarily **lattice-based cryptography** (like CRYSTALS-Dilithium) for efficiency and **hash-based signatures** (like SPHINCS+) for high security confidence. NIST finalized **ML-KEM (Kyber)** for key encapsulation, **ML-DSA (CRYSTALS-Dilithium)** for digital signatures, and **SLH-DSA (SPHINCS+)** for hash-based signatures in 2024. **Falcon (FN-DSA)**, another lattice-based signature scheme, is expected as a separate draft standard but has not yet been finalized. Unlike current systems that rely on the difficulty of factoring or discrete logarithms, these approaches use mathematical problems that remain hard even for quantum computers.

#### Implementation Timeline

Major tech companies, governments, and security organizations are already testing and implementing these quantum-resistant systems. Rather than a catastrophic overnight change, we're looking at a gradual, managed transition over the coming decades.

Critical systems like banking infrastructure, government communications, and power grids will upgrade first, followed by consumer applications. Many organizations are building flexibility into their systems now: the ability to quickly swap out encryption methods like changing the batteries in a device. The goal is that most of these security upgrades can be delivered through regular software updates, though some will require hardware changes too.

While quantum computers pose a real future threat to current encryption, the cybersecurity community is actively preparing solutions. The transition will be gradual and planned, not a sudden crisis.

#### What Makes Cryptography Quantum-Resistant

Before examining how blockchains are adapting, it's important to understand what makes some cryptographic systems more resistant to quantum attacks than others. The key distinction lies in the underlying mathematical problems.

Current public key systems like RSA and ECDSA rely on problems that quantum computers can solve efficiently using Shor's algorithm: factoring large numbers and computing discrete logarithms. These mathematical structures have elegant patterns that quantum algorithms can exploit.

Quantum-resistant cryptography instead uses mathematical problems that remain hard even for quantum computers. These include lattice-based problems (finding the shortest vector in a high-dimensional lattice), hash-based signatures (building security from collision-resistant hash functions), and code-based cryptography (decoding random linear codes). Unlike factoring, these problems lack the mathematical structure that makes them vulnerable to quantum shortcuts.

The NIST-approved algorithms leverage these harder problems. CRYSTALS-Dilithium and Falcon use lattice mathematics, while SPHINCS+ builds on hash functions. Each offers different trade-offs between signature size, speed, and security assumptions. This diversity provides insurance: if one mathematical approach proves vulnerable, the ecosystem can shift to alternatives.

With this foundation in quantum-resistant techniques, we can now examine how blockchain networks must navigate the unique challenges of migrating entire decentralized systems to these new cryptographic standards.

## Section II: Blockchain Vulnerability Assessment

Blockchains face a uniquely difficult challenge in the quantum era. Unlike traditional systems where organizations can mandate centralized upgrades to post-quantum cryptography, blockchain networks operate through distributed consensus among thousands of independent nodes. The very features that make blockchains secure today (immutability, transparency, and decentralization) become obstacles when coordinating a cryptographic migration.

The challenge intensifies because blockchain transactions create permanent public records. Every signature ever published on-chain becomes a potential attack surface once quantum computers mature. Traditional financial systems can rotate their encryption keys behind closed doors, but blockchain addresses with exposed public keys remain vulnerable forever unless protocol-level changes intervene. This section examines which blockchain assets face the greatest quantum risk, why some addresses are more vulnerable than others, and what users can do to protect themselves while developers work on network-wide solutions.

### Technical Foundation

Most blockchain networks rely heavily on elliptic-curve signatures for security. Bitcoin and Ethereum use **ECDSA over secp256k1**, while Solana employs **EdDSA over ed25519**. These signature schemes derive their security from the **Elliptic Curve Discrete Logarithm Problem (ECDLP)**, which presents an insurmountable challenge for classical computers but becomes trivial for Shor's algorithm running on a sufficiently powerful quantum computer.

It's crucial to understand the different attack vectors: Grover's algorithm provides quadratic speedup for preimage and second-preimage attacks on hash functions, while the best-known quantum collision attack (**BHT**) scales around 2^(n/3), offering a different and generally weaker advantage than Grover's preimage capabilities. While 128-bit security remains computationally infeasible today, it necessitates larger hash outputs for equivalent protection in a post-quantum world.

To illustrate the threat landscape: Shor's algorithm is like a master locksmith who can reverse-engineer any lock's blueprint from its face (the public key) and cut a matching key directly, catastrophic for RSA and ECDSA once the tools mature. Grover's algorithm resembles a superhuman librarian who must still search through library stacks, but can do so far more efficiently, turning a 256-bit search space into an effectively 128-bit one. One breaks mathematical structure entirely; the other dramatically accelerates brute-force search.

### Public Key Exposure Models

Think of it like this: a Bitcoin address is like a safe whose combination (the public key) isn't revealed until someone opens it. Once the safe is opened, anyone listening can record the combination. Today's eavesdroppers can't use that combination to break into safes, but when quantum "lockpicks" arrive, they can replay those recorded combinations to steal whatever remains inside.

This analogy captures a fundamental principle: quantum computers can break public keys, but they cannot easily break the cryptographic hashes of those keys. This distinction determines which funds are at risk.

### Why Legacy Bitcoin Addresses Are More Vulnerable

Legacy Bitcoin addresses face significantly higher quantum risk for two concrete reasons. First is direct public key exposure through **P2PK** outputs. Early Bitcoin (2009-2012) frequently used P2PK (Pay-to-Public-Key) outputs that publish the public key directly on the blockchain with no cryptographic protection.

The transaction literally says "here's the public key, anyone who can prove they control it can spend this." Over 1.5 million BTC (roughly 8.7% of Bitcoin's total supply, yet only 0.025% of UTXOs) remain locked in these completely exposed P2PK outputs, including Satoshi's early mining rewards. This is like having a safe with the combination written on the outside. Quantum computers won't need to break any locks; they can simply read the combination and walk in.

The second vulnerability comes from address reuse patterns. Early Bitcoin users commonly reused the same address for multiple transactions, a practice that was later discouraged. Each time someone spends from an address, they expose its public key on the blockchain. With address reuse, the first transaction reveals the public key while subsequent transactions leave remaining funds vulnerable to quantum attack. Legacy users often accumulated large balances on single addresses over time, then only spent portions, leaving substantial "change" vulnerable after the first spend.

### Current Standards

Newer Bitcoin addresses use **P2PKH** (Pay-to-Public-Key-Hash) and **P2WPKH** formats that only store the hash of the public key on-chain. The actual public key remains hidden until spending. Combined with modern single-use address practices, this creates much stronger quantum resistance. Unspent modern P2PKH and P2WPKH addresses keep their public keys never exposed and thus remain quantum-safe. Single-use spending patterns expose the public key only after funds are moved, leaving no remaining balance to attack.

However, **P2TR (Taproot)** addresses present a different exposure pattern. Taproot key-path spends embed a public key directly in the output, placing them in the "exposed-key" category similar to P2PK. While Taproot currently holds a relatively small share of Bitcoin's total supply, users should be aware that these addresses don't provide the same quantum protection as P2PKH or P2WPKH.

Ethereum's account model creates different exposure patterns. Every transaction from an **EOA** exposes a recoverable public key, but accounts that have never sent transactions remain protected. However, once an Ethereum address sends its first transaction, the public key is permanently exposed for any future deposits to that same address.

While individual address management presents clear challenges, smart contract wallets may offer enhanced protection through proxy patterns and upgradeable implementations, potentially enabling migration to quantum-safe signature schemes without changing the wallet address. However, this protection depends entirely on specific implementation details and available upgrade mechanisms.

Multi-signature wallets present complex migration challenges, typically requiring all signers to coordinate simultaneous upgrades to post-quantum schemes. Social recovery mechanisms might provide alternative migration paths, though these require careful design to maintain security assumptions.

### Dormant and Potentially Lost Wallets

Building on these exposure patterns, we can now categorize the specific types of vulnerable assets across the ecosystem. **Dormant addresses** with exposed public keys represent significant systemic risk to the broader ecosystem.

The vulnerable landscape includes early adopter addresses with potentially lost private keys but exposed public keys from past spending activity, and abandoned mining addresses from Bitcoin's early era, particularly those used for early block rewards that were subsequently spent, exposing their public keys to future quantum harvest.

The fundamental challenge lies in distinguishing between genuinely lost funds and dormant but recoverable wallets. Quantum attackers could potentially recover funds from addresses presumed permanently lost: imagine the market chaos if millions of "lost" Bitcoin suddenly became recoverable, creating unexpected supply shocks and complex ownership disputes that could destabilize the entire ecosystem.

This creates a high-stakes scenario often described as a "**quantum rush**." Should a powerful quantum computer emerge suddenly, it would trigger a frantic race. Malicious actors would rush to crack susceptible addresses and steal exposed funds, while network developers and the community would race to deploy emergency forks to freeze or migrate those same assets. The outcome of such an event would depend heavily on who acts first, introducing a stark game-theoretic dynamic into the security model.

At current valuations, those at-risk BTC represent over $100 billion in exposed value, effectively creating a massive bounty for whoever achieves quantum supremacy first. This transforms quantum computing development from purely scientific pursuit into strategic competition. Nation-states and well-funded private entities now have a concrete financial incentive, beyond military or intelligence applications, to accelerate their quantum programs: whoever breaks the threshold first gains the ability to seize billions in abandoned or lost Bitcoin before the network can coordinate defensive forks. The race isn't just about who builds the computer, but who can extract maximum value before the window closes.

### Best Practices

To protect against future quantum computing threats, users should adopt careful key management practices. For Ethereum, avoid keeping large amounts of funds in an address after its first transaction, since any on-chain signature reveals the public key to potential quantum attacks. Instead, migrate to a fresh, unused address or preferably a smart contract wallet that can be upgraded to post-quantum cryptographic schemes.

Bitcoin users should similarly avoid address reuse by spending entire **UTXOs** to fresh addresses, ensuring no value remains tied to previously exposed public keys. While multisig and multi-party computation (**MPC**) solutions offer enhanced security today, they don't eliminate quantum risk if they still rely on secp256k1 cryptography once public keys are revealed; their primary value lies in providing an upgrade path to post-quantum algorithms when they become available.

### The Protocol-Level Challenge

While individual users can adopt protective practices, the exposure patterns detailed above reveal a fundamental limitation: personal key management cannot protect the ecosystem as a whole. The over 1.5 million BTC sitting in exposed P2PK outputs, the countless reused addresses from Bitcoin's early days, and Ethereum's account model exposure all require coordinated protocol-level responses. 

No amount of individual vigilance can secure funds whose public keys are already permanently visible on-chain, nor can it prevent the systemic chaos of a potential quantum rush. This reality has driven blockchain developers to move beyond user education toward concrete technical proposals for network-wide quantum resistance. The question is no longer whether blockchains need protocol changes, but rather how to implement them without breaking existing functionality or creating unacceptable economic disruption.

## Section III: Quantum-Resistance Transition

Having established the threat landscape and vulnerability patterns, we now turn to how major blockchain networks are responding. Each network faces unique architectural constraints and governance challenges that shape their migration strategies. Bitcoin must balance immutability with security upgrades, while Ethereum leverages its more flexible upgrade culture. The technical solutions exist, but implementing them requires navigating complex social coordination problems that test the limits of decentralized governance.

### Bitcoin's Approach

The Bitcoin developer community is actively working on concrete plans to protect the network against future quantum threats, with several serious proposals now under review. As detailed in Section II, this effort particularly targets the 1.5 million BTC in exposed P2PK outputs, including Satoshi's early mining rewards, representing a disproportionately large amount of Bitcoin concentrated in a small number of vulnerable transactions.

The technical solutions under consideration are sophisticated, building on Bitcoin's existing upgrade mechanisms. **BIP-360 (P2QRH)** represents a soft-fork that introduces a new "Pay-to-Quantum-Resistant-Hash" address type. The latest draft makes P2QRH a taproot-style, script-spend-only output, disabling key-spends to prevent quantum vulnerabilities. Post-quantum signature opcodes will be specified in a separate future BIP, not inside BIP-360 itself.

This represents a gradual approach that could be adopted without breaking existing functionality. Additionally, developers are exploring ways to leverage **Taproot's** existing structure by disabling key-path spends and adding quantum-resistant signature checks to tapscript.

However, the core challenge isn't technical but social and economic: should Bitcoin force users to migrate, or make it optional? Proposed solutions span a wide spectrum. Jameson Lopp has outlined a multi-year deprecation plan that would gradually phase out at-risk outputs, while Agustín Cruz's more aggressive "QRAMP" protocol proposes hard deadlines for the upgrade, though this faces pushback over potentially making dormant funds unspendable. Other proposals explore commitment schemes allowing current holders to prove ownership and move assets safely, or deadline-based systems with grace periods.

The debate intensifies when considering what should happen to dormant holdings that can't or won't be moved before quantum computers arrive. Three main approaches are under discussion: **(1) permanently burning** the at-risk assets to prevent quantum seizure, **(2) doing nothing** and allowing quantum-equipped actors to claim them, or **(3) recycling** the funds back into the block reward subsidy to extend miner incentives beyond the original supply schedule.

Each option faces significant philosophical resistance within the Bitcoin community. The ethos strongly opposes burning or recycling holdings that are rightfully owned, even if the owner is presumed dead or absent. The principle of immutable property rights runs deep in Bitcoin culture; many view Satoshi's early holdings as legitimately his, and any protocol change that makes them unspendable, whether through burning or redistribution, violates the fundamental promise that "your keys, your coins" means permanent ownership. This creates a painful tension: protecting the network from quantum attack may require violating the very property rights that make Bitcoin valuable in the first place.

Ultimately, for truly lost or abandoned assets where private keys are genuinely gone, developers face this difficult choice: either these funds will be stolen by whoever possesses quantum computing capabilities first, or they will become unspendable through protective consensus changes. While Satoshi himself suggested in 2010 that users could upgrade to stronger cryptographic schemes, this solution only works for those who still control their private keys. No consensus has emerged on timelines or enforcement, but Bitcoin Optech continues tracking these debates as they evolve from early concepts toward potential consensus rules.

### Ethereum's Approach

Unlike Bitcoin's philosophical tensions around property rights and coin burning, Ethereum faces primarily technical scaling challenges. The community's more flexible upgrade culture allows for iterative solutions, though the practical obstacles remain substantial. Current cryptographic primitives, like the secp256k1 ECDSA signatures used by user accounts and **BLS** signatures used by validators, would be susceptible to the attacks discussed earlier.

The upgrade strategy centers on a multi-pronged, staged approach rather than a single protocol-wide switch. For user transactions, **EIP-7932** proposes supporting multiple signature algorithms to enable post-quantum schemes while maintaining backward compatibility with existing accounts. **Account Abstraction** is serving as a key on-ramp, allowing smart wallets to implement these quantum-safe signatures without requiring immediate protocol changes. The Ethereum Foundation is actively funding research into post-quantum multi-signature schemes to address the larger signature sizes that come with quantum-resistant algorithms.

However, these new algorithms come with significant practical trade-offs. The most immediate challenge is the dramatic increase in data size. A current ECDSA signature is approximately 64 bytes, providing a compact baseline for comparison. CRYSTALS-Dilithium signatures are around 2,400 bytes, roughly 37 times larger than current signatures. SPHINCS+ signatures are even more substantial: approximately 7,900 at 128-bit security ('s' variant), around 16,200 at 192-bit security, and can exceed 29,000 at higher security levels. This represents a 123x to 450x size increase over current signatures.

These size increases directly impact blockchain operation in multiple ways. Transactions become larger, leading to increased storage requirements and **blockchain bloat**. Higher transaction fees follow naturally from the increased data that must be processed and stored. Slower verification times can also affect block processing and network throughput, presenting a major engineering hurdle for protocol developers who must balance security against usability.

Beyond user accounts, Ethereum is planning broader architectural shifts toward quantum-safe foundations. The long-term vision involves moving away from pairing-based cryptography (like **KZG** commitments used in data availability) toward hash-based and STARK-style constructions, which only face Grover's algorithm's more manageable quadratic speedup rather than Shor's exponential advantage. An articulated proposal exists for an emergency recovery fork to quickly freeze exposed accounts and provide migration paths if quantum breakthroughs happen suddenly.

This is no longer just theoretical planning. There are draft EIPs in active discussion, Ethereum Foundation grants funding post-quantum research, and working prototypes using Account Abstraction for quantum-safe signatures.

## Section IV: Key Takeaways

**Quantum computers threaten public key cryptography, not all encryption equally.** Shor's algorithm can break the ECDSA and RSA systems that secure blockchain wallets and internet communications, rendering today's digital signatures vulnerable once sufficiently powerful quantum computers emerge. However, symmetric encryption like AES-256 remains secure with only minor key size adjustments, and hash functions like SHA-256 retain adequate protection despite Grover's algorithm cutting their effective security in half (from 256 bits to 128 bits, still computationally infeasible to crack). This distinction matters because it means the blockchain ecosystem needs targeted upgrades rather than complete cryptographic reinvention; the foundation remains solid even as the signature layer requires replacement.

**The timeline uncertainty creates a "steal now, decrypt later" paradox.** While cryptanalytically relevant quantum computers likely won't arrive until the 2030s or 2040s, adversaries can harvest encrypted data today and store it for future decryption once the technology matures. This makes long-term secrets (government communications, proprietary research, personal health records) vulnerable right now, even though the actual decryption capability remains years away. For blockchain users, this means that exposed public keys from old transactions represent a ticking time bomb; once quantum computers achieve sufficient scale, attackers could systematically crack every vulnerable address in a coordinated "quantum rush," racing against network developers trying to freeze those assets through emergency forks.

**Early Bitcoin addresses face existential risk from quantum attacks.** Over 1.5 million BTC sit in P2PK outputs where public keys are permanently visible on the blockchain. There's no cryptographic hash protection, just raw exposure dating back to Bitcoin's earliest days, including Satoshi's mining rewards. Combined with widespread address reuse from 2009 through 2012, these legacy patterns create a clear attack surface: quantum computers won't need to break any locks because the cryptographic keys are exposed publicly. Modern P2PKH and P2WPKH addresses offer dramatically better protection by keeping public keys hidden until spending. However, P2TR (Taproot) key-path spends embed a public key in the output and are therefore in the exposed-key category. The vulnerability isn't inherent to Bitcoin's design but rather to outdated usage practices that can (and should) be abandoned by any user who still controls their private keys.

**Migration requires coordination that blockchain governance wasn't designed to handle.** Bitcoin developers have drafted multiple quantum-resistance proposals (BIP-360 for new address types, Taproot modifications, deadline-based migration systems), but no consensus exists on whether to make upgrades optional or mandatory, how to handle dormant wallets, or whether to burn potentially lost coins before quantum computers can steal them. Ethereum faces similar challenges with EIP-7932 and Account Abstraction serving as migration paths, but the technical solutions come with severe practical costs: CRYSTALS-Dilithium signatures are 37 times larger than current ECDSA signatures, while SPHINCS+ signatures are over 265 times larger, creating blockchain bloat and fee spikes that could price out ordinary users. The cryptography works; the political economy of deploying it across millions of independent actors remains blockchain's hardest unsolved problem.

**User behavior today determines quantum vulnerability tomorrow.** Every transaction that exposes a public key (whether through spending from a Bitcoin address or sending from an Ethereum EOA) creates permanent quantum risk for any future deposits to that same address. Smart practices include treating addresses as single-use, migrating holdings to fresh addresses after any spending event, and preferring smart contract wallets with upgrade mechanisms over basic externally owned accounts. The difference between a quantum-safe wallet and a vulnerable one often comes down to whether the user reused an address after its first transaction; no amount of protocol-level protection can save users from their own key management mistakes, making education as critical as technical upgrades in the race against quantum computers.

The quantum threat illustrates a deeper truth about decentralized systems: **technological security ultimately depends on coordinated human action.** Cryptographers delivered quantum-resistant algorithms through NIST's 2024 standards; developers are building migration paths into protocol layers; but the actual transition requires millions of users to understand the risk, change their behaviors, and potentially accept higher costs, all without the ability to force compliance or freeze assets unilaterally. The blockchain community has roughly a decade to solve a coordination problem that has no precedent in human history, where the cost of failure isn't just broken encryption but the potential collapse of trustless systems that billions of dollars depend upon.