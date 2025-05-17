# Checksum

In a distributed system, while moving data between components, it is possible that the data fetched from a node may arrive corrupted. This corruption can occur because of faults in a storage device, network, software, etc. How can a distributed system ensure data integrity, so that the client receives an error instead of corrupt data?

Calculate a checksum and store it with data.

To calculate a checksum, a cryptographic hash function like MD5, SHA-1, SHA-256, or SHA-512 is used. The hash function takes the input data and produces a string (containing letters and numbers) of fixed length; this string is called the checksum.

When a system is storing some data, it computes a checksum of the data and stores the checksum with the data. When a client retrieves data, it verifies that the data it received from the server matches the checksum stored. If not, then the client can opt to retrieve that data from another replica.

## Checksum use cases

### Data Integrity Checks

Imagine sending a super-secret spy message - you wanna make sure it doesn’t get altered during transmission, right? Checksums ensure data hasn’t been tampered with during transmission by checking - you guessed it - the Checksum! If it doesn’t match, something’s fishy.

### Error Detection

Ever download a file and it just won’t open? Checksums can help detect if a bit of data got scrambled during a download, helping systems know when they need to try downloading it again.

### Data Retrieval and Verification

When you download software or a file from a website, they often provide a Checksum value. You can use this to verify the integrity of the data, ensuring that what you downloaded is exactly what the creators intended, no nasty surprises hiding inside!

### Networking

In networking, Checksums help detect errors in packets of data sent over a network. If the arriving packet's Checksum doesn’t match the one it was sent with, the packet can be rejected, ensuring no corrupted data gets through!

### Secure Storage

In some databases, Checksums help maintain the integrity of the stored data. Periodically, the stored data is checked against the Checksum - if it doesn’t match, the system knows something’s amiss in the storage system!

### Password Verification

Some systems store the Checksum of a password instead of the password itself. When you log in, the system runs the Checksum algorithm on the password you enter and checks that Checksum against the stored Checksum. If they match, you’re in! No need to store actual passwords, adding a layer of security!

### Preventing Accidental Duplicates

Systems can use Checksums to prevent accidentally storing duplicate data. If two pieces of data have the same Checksum, they might be duplicates, saving storage space and preventing redundancy.

