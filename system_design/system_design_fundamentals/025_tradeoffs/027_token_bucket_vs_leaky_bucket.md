# Token bucket vs leaky bucket

Token Bucket and Leaky Bucket are two algorithms used for network traffic shaping and rate limiting. They help manage the rate of traffic flow in a network, but they do so in slightly different ways.

![image](https://github.com/user-attachments/assets/a3ba71cd-4603-46b0-b56a-6e104f94dd35)

## Token bucket algorithm

The token bucket algorithm is based on tokens being added to a bucket at a fixed rate. Each token represents permission to send a certain amount of data. When a packet (data) needs to be sent, it can only be transmitted if there is a token available, which is then removed from the bucket.

### Characteristics

- Burst Allowance
  - Can handle bursty traffic because the bucket can store tokens, allowing for temporary bursts of data as long as there are tokens in the bucket.
- Flexibility
  - The rate of token addition and the size of the bucket can be adjusted to control the data rate.

### Examples

Think of a video streaming service. The service allows data bursts for fast initial streaming (buffering) as long as tokens are available in the bucket. Once the tokens are used up, the streaming rate is limited to the rate of token replenishment.

### Pros

- Allows for flexibility in handling bursts of traffic.
- Useful for applications where occasional bursts are acceptable.

### Cons

- Requires monitoring the number of available tokens, which might add complexity.

## Leaky bucket algorithm

In the leaky bucket algorithm, packets are added to a queue (bucket), and they are released at a steady, constant rate. If the bucket (buffer) is full, incoming packets are discarded or queued for later transmission.

### Characteristics

- Smooth Traffic
  - Ensures a steady, uniform output rate regardless of the input burstiness.
- Overflow
  - Can result in packet loss if the bucket overflows.

### Examples

Imagine an ISP limiting internet speed. The ISP uses a leaky bucket to smooth out the internet traffic. Regardless of how bursty the incoming traffic is, the data flow to the user is at a consistent, predetermined rate. If the data comes in too fast and the bucket fills up, excess packets are dropped.

### Pros

- Simple to implement and understand.
- Ensures a steady, consistent flow of traffic.

### Cons

- Does not allow for much flexibility in handling traffic bursts.
- Can lead to packet loss if incoming rate exceeds the bucket’s capacity.

## Token bucket vs leaky bucket

- Traffic Burst Handling
  - Token bucket allows for bursts of data until the bucket's tokens are exhausted, making it suitable for applications where such bursts are common. In contrast, the leaky bucket smooths out the data flow, releasing packets at a steady, constant rate.
- Use Cases
  - Token bucket is ideal for applications that require flexibility and can tolerate bursts, like video streaming. Leaky bucket is suited for scenarios where a steady, continuous data flow is required, like voice over IP (VoIP) or real-time streaming.

Choosing between Token Bucket and Leaky Bucket depends on the specific requirements for traffic management in a network. Token Bucket offers more flexibility and is better suited for bursty traffic scenarios, while Leaky Bucket is ideal for maintaining a uniform output rate.

