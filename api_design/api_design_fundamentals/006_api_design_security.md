# API design security

## API design security intro

We need application security (both client and server side) and data security (both at rest and in transit). Therefore, API security becomes a combination of all these security methods plus network security:

<img width="341" alt="image" src="https://github.com/user-attachments/assets/4d808f9b-3978-4eed-ab40-32e59f54ba47">

As time goes on, the number of digital attack surfaces are increasing. There are numerous methods through which malicious users may attack, the primary methods being as follows:

- Distributed denial of service: This is when multiple machines target a specific entity in our system by overloading it with requests to disrupt its regular functioning. The attack traffic in this method is usually in the form of a botnet.

Note: A botnet is a group of exploited machines altered due to malware. Such machines combine to create a network of bots to work on an attacker’s agenda.

- Insufficient authentication: When our clients aren't adequately authenticated (the procedure through which our API verifies who the user is), our API may receive bogus or potentially malicious calls that may hinder its functionality and lead to issues in access control.

- Injections: When malicious code is entered into our system, it endangers the data present in our API along with access control. This is most commonly done through cross-site scripting (XSS) or SQL injections, which we’ll expand on in an upcoming lesson.

- Exposed data in API calls: When transferring data, an attacker may intercept the data and impersonate one of the parties, which is known as the man-in-the-middle attack. This can lead to the impersonator gaining unauthorized access to our data, which could lead to devastating consequences.

The diagram below illustrates the surfaces where these attacks may occur from:

<img width="558" alt="image" src="https://github.com/user-attachments/assets/33b26d25-942f-4a36-8bdd-146b0f0b3be4">

If you're well-versed in the API landscape, it should come as no shock that security is often overlooked. Developers are constantly adopting new security mechanisms related to API practices, but there will always be vulnerabilities for attackers to uncover. It's much easier and resource effective to consider security at the inception of the API's design and scale it as time goes on rather than retrofitting to an already finished API later in its lifecycle. There are many aspects that should be contemplated when designing a secure API, namely the ones mentioned in the illustration below:

<img width="554" alt="image" src="https://github.com/user-attachments/assets/9a8b74c4-293d-4bf2-8107-a76aa8d28a5d">

### Assets

Assets are considered to be the sensitive data and entities that need to be protected. This may include physical devices that our API depends on, such as application and caching servers, databases, or digital entities (the data stored in our API). Physical assets are easy enough to guard with the use of security cameras and whatnot, but protecting our virtual data from harm is a different fight altogether. The inability to protect these assets could lead to reputational and financial damage. So, we define some goals to prevent such situations.

### Security goals

Our primary security goal should be the protection of these assets, most commonly defined through the CIA triad. The CIA triad is a general security model that has been employed for decades. This triad is represented by three components that lay the groundwork for our design principles and implementations.

<img width="425" alt="image" src="https://github.com/user-attachments/assets/a4cd1bce-c75e-47fb-b8f6-3f12e439523c">

The three factors are as follows:

- Confidentiality: This refers to the guidelines and regulations administered that make sure that only authenticated users have access to relevant information. Enabling secrecy and privacy serves as the primary goal of confidentiality.

- Integrity: This aspect ensures that the information present is accurate and reliable and not tampered with in any way, whether it be intentional alteration by attackers or data corruption in transmission.

- Availability: This feature guarantees that the users we have validated have a constant entry point to the data they wish to access. More plainly, it refers to our servers, machines, and applications being in a constant state of functioning, so our authorized users can access our resources in a convenient manner.

<br/>
<br/>

What is a real-life example that highlights all three principles of the CIA triad?

An ATM commonly displays all principles of the CIA triad. Its PIN code reflects confidentiality, its logging of all deposits and withdrawals preserves the integrity, and its machines being publicly accessible anywhere demonstrates its availability.

### Threat modeling

It's imperative that we define the threats faced by our API in the environment in which we run it. As with any entity that allows public access to its resources, it provides an attack surface for malicious actors to exploit. These attack surfaces only increase as the usage of API becomes commonplace, leading many to speculate that API attacks may become the most relevant attack vector in the future.

The set of threats relevant to our API is defined as our threat model, which can be classified through the STRIDE acronym, which is expanded on in the table below:

<img width="448" alt="image" src="https://github.com/user-attachments/assets/76e8bc3a-0a42-4c5c-a123-f96bcfb616e6">

The process of threat modeling is as follows:

1. Curate a system diagram highlighting the primary entities (such as clients and endpoints) in our API, and pinpoint the trust boundaries of each component.

2. Identify information flow between the system entities, and model it as directed arrows.

3. For each trust boundary drawn in the prior steps, map out potential threats to our security goals, perhaps by referring to the STRIDE model.

4. Select mechanisms that aid us in achieving our security goals to combat threats defined in the STRIDE model. We record these threats to guarantee that they are kept track of in the development lifecycle.

Note: A trust boundary is defined as the area in which all encompassed entities trust each other.

An example of a threat modeling diagram is given below:

<img width="489" alt="image" src="https://github.com/user-attachments/assets/f09bbf8d-9271-434e-a246-cde7f6afc9c5">

Note: The API and database have separate trust boundaries to avoid the risk of a compromised API accessing sensitive information present in the database.

Depending on the nature of the API, we may decide to concentrate our efforts on a specific aspect of security. For example, if our API exclusively handles sensitive user data, we need to emphasize security measures that protect this information. On the other hand, if the data isn't sensitive and can be accessed publicly, the same measures aren’t required to protect the data. Through threat modeling, we aim to uncover gaps in our system and in turn, bolster our defenses against these threats by utilizing security mechanisms that deal with a particular security need.

### Mechanisms

Now that we've mapped out the threats with the modeling mentioned above, we require sufficient means to secure our APIs. To guard against these attacks, we have to implement security mechanisms that can be found in any well-developed API.

To guarantee that a certain security goal is met, we apply the following mechanisms, among others:

- Encryption: While most mechanisms protect access to the API itself, encryption secures data whilst it's transmitted over the network between applications. This mechanism fulfills the confidentiality aspect of the triad so that even if the data is intercepted, it'll be useless to unauthorized users without the correct decryption methods. Primarily in API design, TLS is used to secure the transfer of data over networks. It aids in integrity and confidentiality.

- Validation: This is the process through which we verify the data entering the API itself. It's an essential aspect that prevents tampering and information disclosure and should be implemented in every API. It aids in confidentiality.

- Authentication: Through authentication, we can verify whether an actor is authorized. When implemented correctly, it nullifies the spoofing and elevation of a privilege threat in which users pretend to be somebody they're not. It aids in confidentiality.

- Authorization: This aspect serves to protect both the identity and confidentiality of our clients, as stated in the CIA triad. This strives to strengthen access control, through which threats such as tampering should be rendered obsolete.

## TLS (Transport Layer Security)

Transport layer security (TLS) is a cryptographic protocol that permits safe transmission between the client and API provider. TLS ensures message authentication, encryption, and data integrity.

In a client-server communication, the server usually requests authentication from clients using sensitive credentials, like a username and password, an API key, and tokens (we’ll explore these techniques in the coming lessons). However, using TLS, the client is able to authenticate the server prior to client authentication. TLS achieves this with the help of digital certificates that a client receives directly from the server.

Note: Digital certificates, also known as public key certificates, are files used by applications to verify their identity and authenticate themselves. This certificate is lodged into the application itself and is used to authenticate itself to the end users that may access the application.

What is the difference between TLS and SSL?

TLS is an enhanced version of SSL. The terms are generally used interchangeably in the industry due to them both establishing secure connections. They primarily differ in how they communicate and establish the handshake between the client and the server. Generally, TLS is assumed to be secure due to it being standardized by Internet Engineering Task Force (IETF).

<br/>
<br/>

Right now, it may appear that encryption is TLS’ most essential feature. However, the identification and the subsequent prevention of attacks are just as important. Encryption isn’t of much use if we aren’t sure of who we’re talking to, as an attacker may be altering the transmission. Therefore, before we dive into the details of the functionality of TLS, let’s jog our memory of the following:

Symmetric and asymmetric cryptography:

Asymmetric encryption, also known as public key cryptography, is primarily used for the exchange of symmetric keys. It differs by utilizing both a public and a private key, one of which is used for encryption and the other for decryption. As the name implies, the public key is shared openly.

The process is as follows:

<img width="521" alt="image" src="https://github.com/user-attachments/assets/df96880f-abd5-4ebe-a854-186f7a97f825">

1. The server sends the public key to the client (public key exchange).
2. The client uses this public key to encrypt its messages and forward them to the server.
3. The server decrypts the message with the use of its private key.

Since the private key is only accessible by the server, no other entity can read the message. Asymmetric cryptography is considerably slower with large key sizes (typically between 1024-4096 bits) since it is based on complex mathematical computation. Therefore, if data is encrypted using this method, the transmission will be slow.

Note: It makes sense to share a symmetric key via asymmetric encryption, which is used for the encryption of application data. This approach not only enables the secure transmission of keys but also improves performance. The generation and sharing of the symmetric key is done through the Diffie-Hellman key exchange. Through this algorithm, the client and the server end up with the same shared key.

Public key infrastructure:

Public key infrastructure (PKI) is a set of policies and procedures required to create, distribute, and utilize digital signatures. It’s involved in the management of asymmetric (public key) encryption. It has the following properties:

1. Its purpose is to transfer information in a secure manner.
2. It binds public keys with their respective entities (client/server).
3. It provides authentication through digital signatures and confidentiality through encryption.

These certificates are administered by a 3rd party certification authority (CA) which is trusted by a bulk of web servers. The CA verifies the legitimacy of the information provided by a requesting entity based on which a digital certificate is provided to that entity. The digital certificate binds the provided information and a public key to the requesting entity.

The diagram below illustrates how a server receives a certificate from the certification authority:

<img width="521" alt="image" src="https://github.com/user-attachments/assets/9b5fa9f9-f550-4430-a2ea-1ef11490341f">

PKI ensures that the public key is distributed correctly by verifying the application’s certificate through the relevant certification authority (CA). Certification authorities are responsible for issuing digital certificates, which are embedded with the public key. These certificates are only valid for a limited time, after which they have to be reissued using the same method above.

Note: Certificates are the way that servers/applications authenticate themselves to the clients so that the clients can trust them with their data.

However, how can a client be sure that it is really talking to a CA to get keys for the API server? To solve this issue, browsers come loaded with top-level CAs keys and certificates, which verify their legitimacy.

### TLS functionality

As we observed above, asymmetric encryption is too slow to be used for data encryption, whereas symmetric encryption has no built-in mechanism for secure key exchange between two parties. Therefore, TLS combines both symmetric and asymmetric encryption in establishing the handshake protocol between the client and server.

Note: The handshake protocol is when both parties exchange the information required to establish secure communication between them.

Note: Asymmetric encryption will be utilized for secure exchange of symmetric keys, which in turn encrypts the data. With this strategy, we can now guarantee confidentiality of messages exchanged between clients and servers.

We'll now explore how TLS functions:

<img width="517" alt="image" src="https://github.com/user-attachments/assets/a4428f2f-3384-4e40-9995-e8440ee711b6">

1. The client sends an initial message to the server. The message contains its TLS/SSL version, along with the client random (a string of randomized bytes) and the cryptographic algorithm it supports.

2. The server then responds with a cryptographic algorithm chosen from the list it obtains from the client, its session ID, the server’s random, and its certificate, which contains an asymmetric public key for encryption purposes (public key exchange). The hash for the entire communication up until the server hello message is encrypted with the server’s private key to produce a digital signature. Because no other entity is in possession of the private key, only the server can produce the signature. Therefore, the client can be sure of the message’s authenticity through these digital signatures.

3. The client verifies the validity of the certificate provided through the relevant certification authority, which confirms the authenticity of the web server. This is how the server authenticates itself to the client.

4. Client authentication into the server is optional because it’s usually handled outside the TLS protocol. Here, the digital signature is how the client verifies the server’s message authenticity. The server and client authenticate each other’s identity in steps 3 and 4.

Note: The client and server random (both are strings) are used to calculate the digital signature. A digital signature proves the authenticity of the server to the client. Also, it validates that the data between the client and server hasn’t been tampered. If an attacker attempts to alter any information, the client will not be able to validate the digital signature, and the handshake will have to be restarted.

5. The client generates another string called the premaster secret, which is then encrypted through the server’s public key and sent to the server. The server decrypts the premaster secret by using the corresponding private key. Now both parties can generate the shared symmetric key by using the server random, client random, and the premaster secret, arriving at the same result. The generated symmetric key derives aspects from both the client and the server, making it unique, by incorporating their randoms (the client random and server random). This is the process through which the symmetric key is securely obtained on both sides.

6. The client sends a “finished” message that indicates the client’s end of the handshake is complete. This is the first message that is encrypted with the shared secret key.

7. The server responds with its own “finished” message that indicates that the server’s end of the handshake is complete. The server and client can now freely exchange any application data that will be encrypted through the shared symmetric key.

Note: The generated symmetric key is only valid for that particular session and will have to be generated again if the session ends. For instance, if the client closes the application through which it established the connection, it would have to go through this entire process again the next time it opens the application. This is done to prevent any security vulnerabilities that attackers may exploit.

TLS handles message integrity by making use of message authentication codes (MACs). A MAC ensures that the message hasn't been altered during transmission, usually with secure hash functions (such as SHA 256). Hashed MACs (HMACs) differ in that they specifically utilize secret keys, which are present at both the client and the server, to hash the data. The process is illustrated below:

<img width="553" alt="image" src="https://github.com/user-attachments/assets/b66ed85e-0486-449f-9587-864dd6390ce0">

The hash generated through the use of a secret key is appended to the original message. This concatenated entity is then encrypted by the shared symmetric key. This message is sent to the client, which decrypts this message, calculates its own hash of the message (using the secret key), and compares the two hashes. If they aren't identical, the message has been tampered with and is discarded. The client may then request the message to be sent again. This is the process through which message integrity is upheld in TLS.

### TLS summary

TLS answers all the questions we presented at the beginning of this lesson:

- How does the client know that the server it’s talking to is exactly the one the client intended? Through the use of digital certificates, the client and server are identified.

- How do we achieve confidentiality/secrecy of the messages? Confidentiality is achieved with the encryption protocols implemented because even if an attacker intercepts a transmission, they won't be able to comprehend or decrypt the ciphertext.

- How does the client know about the integrity of the message it has received? Integrity is achieved when the receiving party checks the MAC to see if the message has been altered.

- How do we verify the authenticity of messages received from the server? The client can be sure of the server's message authenticity by evaluating digital signatures.

### HTTP vs HTTPS

Before TLS, HTTP protocol was the standard for web communication due to its lightweight nature. However, it forwards data over the Internet in plaintext, which causes it to be insecure and susceptible to attackers.

When we communicate through HTTPS, we are provided with another layer of security, which is provided through SSL/TLS. This not only transmits encrypted data instead of plaintext, but it also uses TLS for supplementary defenses. The usage of these protocols causes it to be heavier than HTTP, which leads to poorer performance.

Let’s say we send a GET request to an entity. If the HTTP protocol was used and the attacker intercepts the transmission, they'll obtain the request similar to the following:

<img width="559" alt="image" src="https://github.com/user-attachments/assets/91b79fde-56cc-43e5-8cf7-21de79025d7a">

However, if HTTPS were used, the attacker would obtain something similar to the following:

<img width="563" alt="image" src="https://github.com/user-attachments/assets/ec46134c-1348-44df-bc14-d7bceddaf7f9">

The unsecured nature of HTTP has caused it to be overtaken by HTTPS because virtually all communication on the Internet is encrypted in some way, usually through TLS.

Both protocols can be compared in the table below.

<img width="481" alt="image" src="https://github.com/user-attachments/assets/05ee50b6-5df2-4ea6-9fe2-270e372baa27">

### TLS conclusion

The introduction of TLS in applications for security induces little performance degradation. However, with its advantages, it's a no-brainer to implement TLS into our API's communication with web servers/clients. Newer versions of TLS support techniques that speed up the handshake process, such as TLS False Start, which allows the client and the server to begin communication before the handshake is completed. The issue is that TLS False Start isn't compatible with all TLS clients and servers due to poorly implemented servers. Therefore, False Start can be used to increase performance, but only if certain conditions are met.

These developments associated with TLS have allowed the computational costs and load times to be negligible, which is critical in regard to API design.

Note: Nowadays, it’s recommended to use TLS 1.3 because it has better performance and is more secure than its predecessors. It does this by reducing round trip times and dropping support for older vulnerable cryptographic algorithms.

## Input validation

We'll explore two types of input validations: client validation and server validation. Before we learn about these validation techniques, let's define the threats we aim to defend our APIs against. The most common API attacks are specified in the table below:

<img width="734" alt="image" src="https://github.com/user-attachments/assets/b0f1d9ab-d7d0-4353-901f-0c3f5f8a647a">

In the following sections, we’ll explore client- and server-side input validation and learn how it aids in preventing various attacks mentioned above.

### Client-side validation

Typically, data inputted through the client side can never be trusted because a careless user is much more common than a malicious one; therefore, client-side validation is implemented in the browser. To combat errors, a response is instantly fed back to the user in real time, most commonly by highlighting the error and displaying the subsequent message. This is usually implemented through a client-side scripting language such as JavaScript, which is considered the industry standard for validation on the client's end.

Note: On the web, we'll typically encounter two types of client-side validation. The first is JavaScript validation, which is entirely customizable but has to be built from the ground up. The second is built-in form validation, which utilizes aspects of HTML and performs better but is less flexible (in terms of implementation) than its JavaScript counterpart.

Consider Educative's own website:

<img width="313" alt="image" src="https://github.com/user-attachments/assets/0a46b3f7-26e9-4820-b58e-089e1b3a09cc">

The “Name,” “Email,” and “Password” fields are instantly highlighted in red because they didn’t pass the validation check implemented in the system. If an email or password is inputted in an incorrect format (an email without the @ for example), we would be presented with a similar response. In our API design, we can implement responses akin to these to inform the user what went wrong.

The following code snippet illustrates a primitive example of how the validation on the "Email" field above may be performed:

```js
function emailValidation() {
  let entity = example.forms["Form"]["email"].value;
  if (entity == "") {
    alert("E-mail is a required field");
    return false;
  }
}
```

Client-side validation not only bolsters security but also lightens the load on the server because it prevents incorrect data from reaching the server through communication channels. However, this doesn't mean that the server doesn't perform its own checks on the data it receives because it's good practice to have both validation schemes working together.

As we can see, all input validation is implemented primarily in the user’s browser. It's not completely secure as the attacker can bypass our scripting language and forward dangerous input to the server.

Therefore, we need another layer of input validation, which is known as server-side validation.

<br/>
<br/>

How can an attacker bypass client-side input validation?

Client-side validation isn’t foolproof because an attacker can easily modify the client-side code through developer tools. Therefore, implementing validation solely on the client side is not advised. It would make our API vulnerable and lead to dangerous exploits.

Conceptually, it is the same when an OS verifies the arguments of a system call before acting on it, even though it was validated (probably by the language runtime) before calling the system call.

### Server-side validation

The server side performs additional checks on the inputs cleared by the client. Typically, a combination of checks are utilized to verify this data, some of which are stated in the table below:

<img width="716" alt="image" src="https://github.com/user-attachments/assets/96bee8bd-0f32-493d-b3c5-771e2ddba2d5">

These checks could also be implemented on the client side, where an application may block a user from inputting alphabetic characters in a phone number field. However, it's still good practice to also administer these checks at the server because it serves as the last line of defense against potentially malicious entries.

The most popular example of this is when websites ask us to create a strong password. It validates whether the input is of the correct size, is alphanumeric, and in some cases, requires special characters. The password entered by the user is validated on the server end, and a response is given to the user corresponding to whether the rules defined were met.

<br/>
<br/>

Why is client-side validation required when we already utilize server-side validation?

Client-side validation is needed to reduce user latency because they’ll get an instant response if incorrect values are entered, leading to a better user experience.

Client-side validation is also needed to reduce the strain on the server because it can reject incorrect data it detects without the need for it to be sent to the server. Therefore, it avoids calling the server for trivial checks that would be a waste of its resources. Not only is it a good user experience, but client-side input validation is also real time.

If we have to perform input validation only on one side, which is the preferred side?

Server side is the preferred side because it’s impossible for malicious users to alter it easily.

## CORS (Cross-origin resource sharing)

With the introduction of JavaScript and Document Object Model (DOM) in web browsers, manipulating an HTML document's objects and properties using JavaScript became possible. As a result, a malicious script loaded by one web page could interact with the resources from another web page and retrieve sensitive information using the latter's DOM. This vulnerability of the DOM could be exploited by forgery attacks, such as a CSRF attack, through which attackers could gain unauthorized access to different resources.

Note: CSRF - Cross-site request forgery attack, where a malicious request is forged to make it look like it’s been made by a legitimate user. This is used to gain access to private data and perform malicious actions.

Here is an example scenario:

Suppose that John is lured into visiting www.evil-site.com. This site responds with JavaScript code that then makes a call to www.facebook.com, where John logs in without any hesitation. As a consequence, the JavaScript code downloaded from www.evil-site.com obtains access to the DOM elements of www.facebook.com and, by virtue, to John's sensitive data.

### The origin problem

The example that we saw above demonstrates an unrestricted interaction between two web pages belonging to different origins, which could lead to a potential data breach. An origin is defined as a combination of scheme (protocol), hostname, and port number (if specified). Two URLs are said to have the same origin if and only if they have the same schemes, hostnames, and port numbers.

<img width="251" alt="image" src="https://github.com/user-attachments/assets/bbfb912c-1646-47bd-973f-27fed08c0d91">

URLs with different hostnames belong to different origins. A request that spans across different origins is known as a cross-origin request.

### The same-origin policy (SOP)

To combat this susceptibility and reduce attack vectors, the engineers at Netscape defined a rule called the same-origin policy (SOP), whereby two web pages can only interact with each other if they belong to the same origin. Simply put, the URL www.evil-site.com can’t access the resources of www.facebook.com since they both have different origins.

The illustration below depicts a same-origin request, where the URL http://abc.com retrieves an image it needs to display by requesting data from its own web server.

<img width="467" alt="image" src="https://github.com/user-attachments/assets/ac488291-7c3f-4ef9-9270-5b473f2e2a17">

Since the origin of the web document and the requested image is the same, the request will be successful. If a server only allows requests from its origin, it follows the SOP.

### The cross-origin resource sharing (CORS) policy

However, in today's world, it isn't feasible to not allow requests from other origins. The SOP is too restrictive, so we need a method that relaxes the constraints imposed by SOP. One such technique is cross-origin resource sharing (CORS), which allows websites to bypass the SOP by going through checks. CORS employs an HTTP header-based mechanism to inform the web browser whether an application belonging to one origin can access resources from a server at a different origin.

CORS allows two types of cross-origin requests: simple and preflighted. Let's begin with simple requests.

#### Simple requests

A simple request meets all the following conditions:

- The request must have an HTTP method.

- The request should have headers that can be defined manually in header variables.

- The only allowed values for the Content-type headers should be defined in the request.

- The upload request object has no registered event listeners.

- No ReadableStream object is used in the request.

Note: Readable streams are a stream of bytes that are utilized in operations where data is read. Examples of such operations are file reading or video streaming.

The process begins with a cross-origin request initiated by http://abc.com for data stored in the http://xyz.com server. In this example, while http://abc.com is a web service, in our context, it will act as a client. The request contains the client's Origin. A response is then sent from the server to the browser. The server adds an Access-Control-Allow-Origin header to the response. The browser then compares the Origin in the client's request with Access-Control-Allow-Origin in the server's response. If they are identical, the cross-origin request is permitted. An example of this situation is shown below:

<img width="527" alt="image" src="https://github.com/user-attachments/assets/0b69f847-63fb-4eb4-971b-51e72d907575">

As we can see in the example above, the application's Origin: http://abc.com is present in the server's Access-Control-Allow-Origin header, which means the cross-origin request will be approved.

It may be helpful for us to see the structure of these requests and responses. Here is what the CORS request would look like:

<img width="556" alt="image" src="https://github.com/user-attachments/assets/b872426c-1f84-47fa-972a-d7d4939a52c9">

The server may send the following response to the request mentioned above:

<img width="556" alt="image" src="https://github.com/user-attachments/assets/522d28d2-cd43-431c-a334-944654cf8118">

Because the Origin header in the request and the Access-Control-Allow-Origin header in the response match, the request will be approved. In comparison, let's look at a server response where an origin is not allowed to access the resource:

<img width="554" alt="image" src="https://github.com/user-attachments/assets/0578c697-fd2b-403e-9731-a9f2c41fe62f">

In this case, the Origin and Access-Control-Allow-Origin headers don't match; therefore, the request will not be approved. In such a case, the browser won't allow the data to be shared with the client. This results in an error on the client side, and for security reasons (to prevent attackers from exploiting CORS), not much information is given on what went wrong.

Is there a way to allow cross-origin requests from all the origins?

Yes. In very specific cases, the Access-Control-Allow-Origin header may be set to *, which allows any Origin to make the request. This case is known as a wildcard, a keyword that depicts this situation. This cannot be allowed in the real world because of security issues that arise if private data is shared and because most browsers don’t support this wildcard.

### Preflight requests

If a request does not fulfill the conditions for a simple request, it needs to be preflighted. This protocol was given this name because it functions similarly to how passengers must be preflighted before they can onboard the plane. Preflighting our request includes an initial check, which ensures the request is safe to be sent to the server. A common reason for preflighting is that the requests may alter the user's data (this could be on both the client and server side).

The check would be as follows:

1. The browser already knows what requests to preflight and makes an initial request to the server seeking permission to employ the methods. This is done through the OPTIONS method, which specifies the client's Origin and Access-Control-Request-Method (the HTTP request methods it requires, such as POST). This is known as a preflight call. Here is how the preflight request looks in the code:

<img width="563" alt="image" src="https://github.com/user-attachments/assets/305aef6a-f547-4795-894e-666ed96ea9e5">

2. If the server accepts the OPTIONS request, it responds by allowing the client to make requests with the methods they requested. These methods are specified in the Access-Control-Allow-Method header. The response header by the server may look something like this:

<img width="562" alt="image" src="https://github.com/user-attachments/assets/1abf1304-a868-4f65-9e0c-e04d160199f4">

3. After the successful completion of the preflight check, the CORS request can be sent by the client http://abc.com as before. However, this time, the client is allowed to define custom headers or use other defined values for different headers. For example, in this case, the client could set the Content-type header to application/xml. The request would look something like this:

<img width="562" alt="image" src="https://github.com/user-attachments/assets/fc277517-c7e5-49d3-9320-1410c28826d3">

4. The server then responds to the CORS request as it would do normally.

Note: To prevent further overhead in our API, we can cache the preflight for a certain amount of time to prevent unnecessary server requests, which could lead to a potential bottleneck. This means multiple requests can be made to the API in the specified time frame. This is provided in the Access-Control-Max-Age header that’s provided by the server, which stores the maximum time the request can be cached for.

Note: GET, HEAD or POST requests do not need to be preflighted.

### Authentication in preflight requests

By default, both simple and preflight requests don't include authentication through credentials. This can be added by the authorization header in the request or take the form of an authorization cookie. To enable this, we must manually specify the flag withCredentials = true for the request. The Access-Control-Allow-Credentials header in the server's response must also be set as true. Authentication with an authorization cookie is shown in the illustration below:

<img width="527" alt="image" src="https://github.com/user-attachments/assets/b2cc7945-67aa-4472-9c85-c508d43eeaaf">

### CORS disadvantages

Even though many APIs and applications implement CORS to allow communications and access from third parties, vulnerabilities may arise. These vulnerabilities typically stem from the lackluster implementation of CORS without taking the proper security measures. Some major factors that lead to CORS being vulnerable are given below:

- Third-party verification (for clients who use the APIs) is not strict enough. Many APIs may ease their verification to ensure everything functions, which allows attackers to exploit this lack of scrutiny.

- APIs allow access from any other origin. This is typically done to streamline the implementation so that the APIs don't need to maintain a list of the approved parties. This allows malicious origins to access the sensitive resources in the API.

- If an API trusts an origin that is susceptible to injection attacks, an attacker could inject malicious code that utilizes CORS to gain access to sensitive information.

Therefore, with all these vulnerabilities, we should have measures that mitigate these damages.

#### Preventing CORS vulnerabilities

As we can see from the prior section, almost all of these vulnerabilities stem from the incorrect implementation of CORS. So, if we're stringent when we implement CORS in our applications, we should avoid most problems. This can be done in the following ways:

- Stringent verification of all origins. There's a direct correlation between an API's leniency in checking origins and the exploitations that may occur.

- Only allow listed and trusted origins, and avoid access to all subdomains of an entity because attackers may exploit this.

- Avoid using wildcards on networks, sites, and URLs. It will allow access to malicious origins that may gain access to resources. A list of trusted origins should be maintained even if it increases the complexity of the implementation.

- Server-side validation should still be implemented. CORS isn't a substitute for this validation, and any malicious entity that bypasses this should be caught by security mechanisms implemented on the server side. This includes validation against the injection attacks we mentioned in an earlier lesson.

In terms of API security, CORS is a robust option because often, most of our requests are from external sources. It's flexible and allows options for security, such as the wildcard and preflighting, and is considered a boost in security in terms of API design.

## Authentication and authorization

Authentication refers to the procedure through which our API verifies who the user is. Typically, applications fulfill this by implementing a login system utilizing usernames and passwords for verification. There are other techniques for authenticating users in the API paradigm that we’ll explore in this lesson.

Authorization is controlling what the user has access to. This is when applications verify whether the user is even allowed to call the request they are making. For example, we may be authorized to view a Google Doc but not edit it.

<img width="553" alt="image" src="https://github.com/user-attachments/assets/9814c545-f53b-4bab-a424-279262a471f0">

### Authentication and authorization mechanisms

There are several mechanisms we can explore in this section, so let's take a look at those prevalent in today's industry. We'll begin with one that's largely regarded as the simplest, HTTP basic authentication.

#### HTTP basic authentication

HTTP basic authentication is a rudimentary scheme that verifies a client through username and password authentication. It encodes the user's username and password in Base64 and embeds it into its Authorization header. The encoding follows a set template. For instance, a client with the username “Bob” and password “thefarmer” will be embedded in the header as follows:

<img width="560" alt="image" src="https://github.com/user-attachments/assets/082a3535-8b61-433b-b4d6-b2fb49cf1d3a">

Note: The Authorization request header represents the username and password as Bob:thefarmer encoded in the Base64 format. The Basic keyword before the encoded text signifies that this request header is for basic authentication.

Once entered, this username and password are sent to the server, which verifies the user. This process is illustrated below:

<img width="483" alt="image" src="https://github.com/user-attachments/assets/3edbadcd-7944-415d-9097-d9fed3f469e0">

What is the purpose of the realm keyword in the WWW-Authenticate header?

The realm keyword signifies the scope of protection, which simply means that it defines an area for which the user’s login credentials are used. If a user’s credentials are registered on a particular realm, they should be valid for any web page on the same realm.

Why do we encode the username and password in Base64?

As a standard, the usernames and passwords in our HTTP headers should only contain ASCII characters. However, it’s possible that a client’s credential includes non-ASCII credentials, which we can’t embed directly into the header. To solve this issue, we encode the credentials in Base64, which generates a string containing ASCII characters that can be decoded when received by the server to obtain the actual username and password.

An example of this is the character 日, which may be used in a username or password. Because it isn’t an ASCII character, we can’t embed it in our header. However, its Base64 encoded format, 5pel, can be embedded into the header.

The advantages and disadvantages of HTTP basic authentication are as follows:

<img width="689" alt="image" src="https://github.com/user-attachments/assets/8e5280ef-0086-4c96-9a68-e4aee3beef9f">

This method has largely been discontinued in the API landscape because of the drawbacks mentioned above, so we turn to other authentication protocols.

#### API keys

API keys deal with the shortcomings of HTTP basic authentication by replacing the encoded username and password with a generated string. API keys are uniquely generated by the API provider for every consumer/application developer to be used in their applications. It should be noted that API keys are merely strings that identify the application, and they require other security protocols for their secure transmission.

Note: API keys can’t authenticate end users making requests, just the application sending the request. For this purpose, it’s used in tandem with other protocols to implement authentication.

With API key authentication, the application forwards its assigned API key in the header of its request. When the server receives the said request, it looks up the API key in its database in hopes of verifying the application. An example of API key generation is shown below:

<img width="482" alt="image" src="https://github.com/user-attachments/assets/7bc480c4-0b54-4762-9dfb-fa426b3929c0">

Utilizing API keys over HTTP basic authentication has many benefits:

- Unlike HTTP basic authentication, API keys provide applications the option to have multiple keys per account.

- API keys are deemed more convenient than their counterpart, which can be seen in their ability to refresh and regenerate tokens used as API keys.

- Because the API is separate from the user’s username and password, any security breach will be limited to the API. Even if the attacker has a compromised key, they won’t have the user’s credentials.

- API keys can be revoked if need be, for instance, if the keys are compromised.

It's essential to keep API keys a secret because if an attacker gains access to an API key, the server won't be able to differentiate it from the legitimate user.

The advantages and disadvantages of API keys are as follows:

<img width="714" alt="image" src="https://github.com/user-attachments/assets/b157f0d9-3919-4cc7-8268-4e4d4f6987f9">

#### JWT (JSON web token)

A JSON Web Token (JWT) is an open standard that’s a compact and self-sufficient method for safely transferring data between entities in the form of JSON objects. JWTs are a collection of encrypted strings denoting a header, a payload, and a signature that travel through HTTP requests. Unlike the previous protocols, tokens can be used for both authentication and authorization purposes because they carry information about the token's holder.

JWTs are commonplace in the API landscape, especially with regard to the security protocols we explored earlier in this lesson. An example of a decoded JWT's header is shown below:

<img width="555" alt="image" src="https://github.com/user-attachments/assets/8f1133d8-cc52-4d27-b2a0-25f206ebb49c">

The header contains information about the hashing algorithm and the token type. In the case above, HS256 is the hashing algorithm, and the token type is JWT.

Payloads contain statements about the user the token is assigned to, such as its name, issuer, and expiration, among others:

<img width="556" alt="image" src="https://github.com/user-attachments/assets/8284ffd7-aca9-47ed-848e-6182e3fadb7c">

Finally, JWTs additionally include a signature that verifies that the holder of the token is legitimate and that the message hasn't been altered in transmission. To generate the signature, we sign the encoded header, the payload, and a secret (exclusive to the entity generating the JWT) with a hashing algorithm mentioned in the header. The recipient of the JWT will recalculate and compare the two signatures to determine if it was altered during transmission.

An example of signature representation is given below:

<img width="553" alt="image" src="https://github.com/user-attachments/assets/b278a4ed-413a-46df-a2c1-8b16fe924ed8">

Note: The code above is encoded as strings using base64. The header and payload are separated by a period, .. The encoded representation of a token follows the [header].[payload].[signature] template, with the period splitting the header, payload, and signature segments.

<img width="374" alt="image" src="https://github.com/user-attachments/assets/365d22a3-7917-42dc-840e-fb6dc75c9da8">

Tokens are embedded with a time limit, after which they are rendered invalid, and a new token has to be generated by using refresh tokens or authenticating into the server again. 

Note: Refresh tokens allow new tokens to be generated without the client having to authenticate into the server again.

The slides below illustrates the creation and usage of tokens:

<img width="482" alt="image" src="https://github.com/user-attachments/assets/6b675a13-af94-4990-b076-df639b190d2b">

The process is as follows:

1. The client sends an authenticate request to the server with their username and password using HTTP authentication. The application validates the request and then creates a token for the client. In the slides above, the username is exampleuser, while the password is password. A token is sent to the client after generation.

2. The token is stored on the client side and is sent through the HTTP Authorization header to the server when requests are made. The Bearer keyword signifies that this authentication scheme is token based, similar to how the Basic keyword earlier signified how basic authentication was being used. This request can be interpreted as requesting access to the bearer of this token.

3. On arrival of the request, the server verifies the token. On successful verification, the server sends an appropriate response back to the client. In the slides, a GET request is put for the client's username, which is returned after verification of the token and the request.

API keys and tokens may seem similar, but there are a few key differences:

- API keys only serve to identify the client, whereas tokens carry more information with them, such as their source, the identifier, and other metadata. This extra information is helpful for authorization purposes.

- Tokens are structured to contain a header and a payload. API keys are just generated strings.

The frameworks discussed in the upcoming lesson will explore the usage of tokens.

The pros and cons of the techniques we explored in this lesson are compiled in the table below:

<img width="679" alt="image" src="https://github.com/user-attachments/assets/d3dd1ce4-6f44-4bac-8aee-5649687ddf9b">

Before we wrap up, let's take a look at the use cases in which API keys and JWTs may be helpful. In the case of blocking unauthorized traffic to our API, keys should be used because they authenticate the applications making the request. API keys are also used in implementing rate limiting, which controls how many calls a specific application is allowed to an API. They can also be used to filter logs by the specific API key.

In cases where we need secure authorization, JWTs that are used as keys are unable to provide this. This is because JWTs have finer-grained controls as compared to a single key. In projects where we need to identify the end users, JWTs are also preferred because keys only identify the application, not the user making the request.

## OAuth: the authorization framework

Refer to the Educative module on OAuth: https://www.educative.io/courses/grokking-the-api-design-interview/oauth-the-authorization-framework

## Authentication and authentication frameworks: OpenID and SAML

Refer to the Educative module: https://www.educative.io/courses/grokking-the-product-architecture-interview/authentication-and-authorization-frameworks-openid-and-saml

## High level view of security in APIs (Optional)

Refer to the Educative module: https://www.educative.io/courses/grokking-the-api-design-interview/high-level-view-of-security-in-apis





