## Public Key Cryptography

You might have noticed that, when browsing on the internet you will occasionally see different icons to the left of the url bar.

If we go to some random [blog](http://derpturkey.com/), we see an information icon with "Not secure" text.

![not secure](readme/derpturkey.png)

If we click on the icon, we get some scary red text reiterating that our connection is indeed not secure. 

![scary red text](readme/scary-red.png)

 But don't unplug your computer and hide under the bed just yet.  That warning is just telling you that the website's server is using HTTP.  HTTP just means that the traffic is unencrypted and could be intercepted without any real effort (as we'll see shortly).  

In this case, I think the attempt to scare you away from derpturkey.com is a little overblown.  After all, it's just a blog.  You go there, you read the content, and then you leave.  <i>You</i> aren't sending any data, and you certainly aren't sending any sensitive date.

But most browser makers take a 'better safe than sorry' approach to informing users.  However, if you are going to be sending data that you wouldn't want the whole world to see, then you should encrypt your data before you send it--with HTTPS.

Encryption is the difference between HTTP and HTTPS.  Before we get into how all of this works, let's try intercepting some traffic from an HTTP connection and then an HTTPS connection.

### Introduction to Wireshark
In order to to that, we are going to use a very common networking tool called Wireshark.  You can download it for free [here](https://www.wireshark.org/download.html).

Hopefully, after using Wireshark, you'll be just a little bit more paranoid about web security.  Let's just let it run for a minute and see what we get:

(run capture)

Depending on what you were doing, you probably got quite a bit more than you were expecting.  All that output can be overwhelming, so we're going to narrow things down a bit.

Since Wireshark can capture just about everying on your network, we are going to narrow it down.  Let's first look at derpturkey.com, a Javascript coding blog.  We'll first get the ip address

```bash
curl derpturkey.com -v
```
If you look at the first couple lines of output, you will see derpturkey.com's ip address: 50.16.86.72.  We can use this to filter our capture:

```bash
ip.addr == 50.16.86.72
```
![HTTP capture](readme/derpturkey-http-capture.png)

Now try clicking around the webpage and see what happens.  You should see a bunch of packets start to populate your screen.  

If you look at the "protocol" columnn, you will notice that some are TCP and others are HTTP.  If you double-click on one of the packets, you'll get a popup window.  In the top pane of the window, you have five lines.  Each one of those lines is a "layer" in the network.  They go from low-level to high-level.  The first line is the lowest layer, and the last is HTTP.  

This brings us to the so-called "OSI model". The OSI (Open Systems Interconnection) model is an abstraction that is used to understand the different layers in a network-- all the way from wires to cat pictures.

The OSI model has either 7 or 5 layers, depending on who you ask (5,6,and 7 are taken together).  But for our purposes, 5 is fine.  


![osi](readme/tcp-ip-stack.png)
<!-- https://docs.oracle.com/cd/E19683-01/806-4075/ipov-10/index.html

![OSI](readme/OSI.PNG) -->

The higher the numbers go, the more abstract things get.  We spend most of our time at the very top of the OSI model, but it's not a bad idea to know a little bit about the lower layers.

Wireshark gives a good illustration of the 5-layer OSI model:

![wireshark-osi](readme/http-wireshark.png)

Datalink (Ethernet II)
Network (Internet Protocol Version 4)
Transport (Transmission Control Protocol)
Application (Hypertext Transfer Protocol)


We already know a little something about the Network layer (IP), and we'll be playing around with the Transport layer too (TCP)

Feel free to click around, but for now we only care about the Application layer.  

If you expand the Hypertext Transfer Protocol line, you should see some familiar faces.  The kind of request (GET), the different headers, and so on.

In the bottom window we have the raw bytes on the left and the slightly-easier-to-read utf-8 encoding on the right.  These are the chunks that make up the flow of the internet.

Wireshark also allows us to take a look at an entire conversation.  Choose a packet, right-click it, then follow, then HTTP stream.  You should see the whole conversation laid out for you.  

![http-conversation](readme/http-conversation.png)

This packet capture represents the detailed history of our internet browsing.  It's a good thing we didn't send anything important over the wire!

Now let's do the same with with a server that uses HTTPS:

(Note: capture then find the ip address)

```bash
curl google.com -v
curl duckduckgo.com -v
```

```bash
ip.addr == 172.217.8.206  //use duckduckgo, search for network security
ip.addr == 107.20.240.232
```
![tcp-tls](readme/tcp-tls.png)

Here you'll notice a couple differences.  First off, the protocols are different.  Instead of HTTP, we have TLS.  What other differences do you notice? 
    -port, encrypted application data is gibberish

![tcp-stream](readme/tcp-stream.png)

Here we have no idea what information we were sending to the server.  So even if someone had intercepted this, they wouldn't be able to do anything with it. 


### Certificates
But how does this encryption happen?  The answer it: certificates.  Let's go to a webpage that uses HTTPS.

```bash
duckduckgo.com
```

If we click on the "lock" icon to the left of the url bar, instead of scary red text, reassuring green:

![valid certificate](readme/valid-cert.png)

We can continue to find out more if we click on the certificate.  The certificate actually has quite a bit of information in it.  Take a quick look.

It turns out the duckduckgo.com's certificate doesn't just contain information about itself, but also information about the certificate (DigiCert SHA2 Secure Server CA) that is vouching for duckduckgo.com's certificate.

And if we do the same thing with DigiCert SHA2 Secure Server CA's certificate, we find that it was issued by DigiCert Global Root CA.  

Wait, so the same company, DigiCert is issuing certificates to itself?  It turns out that the entire system of credibility that undergirds encrytption on the internet is just a small group of big companies saying that they trust each other--so you can trust who they trust.  Yikes!

But it seems to be working for the moment.  Those top level players are called Certificate Authorities, and all roads lead to them.

The chain of certificates that starts with duckduckgo.com leads up to one of the elect Certificate Authorities, in this case DigiCert Global Root CA.  

Go to you settings in Google Chrome and search for "Manage Certificates".  Eventually you should be able to see all of the certificates from the Certificate Authorities:

![Root CAs](readme/root-ca.png)

Yes, you've had all these certificates the whole time.  Later on, you'll see what happens when that certificate chain has a broken link, and what you might be able to do to fix it.


### Back to HTTPS
Now that we know a little bit about the mechanism that enables trust on the internet, let's get back to our packets.

We saw some TCP packets that preceeded either the HTTP or TLS protocols.  HTTPS adds some extra steps to the initial interaction between a client (browser) and a server. Before sending the application data (OSI layer 7), there is what is called a "TLS handshake".  The TLS handshake is when the encryption is negotiated.

![TLS Handshake](readme/tls_handshake.png)

 The end result of all these steps is an agreement between the client and the browser to use a specific encryption mechanism.  So when you send your credit card number in a form, even if someone intercepts the message (very easy to do as we'll see), there won't be anything useful for a potential attacker to steal.

(Wireshark)

We are going to present a somewhat simplified overview of that negotiation.

// https://www.thesslstore.com/blog/explaining-ssl-handshake/

1. The Server Sends the Certificate to the Client
2. The Client Authenticates the Certificate
3. Negotiate Encryption

#### The Server Sends the Certificate to the Client
Before any application data is sent (i.e. the webpage), an encrypted session needs to be established between the client and the server.  The server is the responsible party here.  It is the server's duty to establish trustworthiness.  

In order to do that, as we've already seen, the server sends along its certificate to establish its identity.  A certificate is basically just a filled out form that is meant to prove that the server is who it says it is.

#### The Client Authenticates the Certificate
What the server sends the client isn't just it's own certificate (called a "leaf", because it is at the end of the "branch"), but a <b>chain</b> of certificates.  The client then checks that the chain leading from the server's leaf certificate all the way up to the Certificate Authority is valid.  That Certificate Authority's root certificate is stored in your browser and/or operating system.

It must ensure that the chain matches, the certificates are not expired, and the certificates have not been revoked.  

It is worth noting here that a valid certificate only establishes the <i>identity</i> of the certificate holder, not moral uprightness.  It's like checking a salesman's driver's licence.  At least it's something.

If the certificate checks out, and the client (browser) trusts that the server is who it says it is, then the client and server can agree on encryption.

The process of nejgotiating encryption is fairly complicated, so let's look at an example first.  


## Ceasar Cipher Example
Let's imagine two secret agents, Alice and Bob.  They live far away from each other, but need to communicate securely.  So they decide to encrypt their letters using a Caesar Cipher--pretty clever.  Anyone who intercepts their letters will just see gibberish.  

But there is a problem.

If Alice want to exchange encrypted letters with Bob using a Ceasar Cipher, they both need to have the same secret key to encode/decode the letter.  But how can Alice tell Bob what the secret key is?  If she simply writes the key in the top corner of the letter, anyone who intercepts the letter will be able to decode it.  

A real conundrum, but there might be a way around it.  Alice thinks about establishing a dead-drop that she and Bob both know about, where she can write the secret key in chalk above a certain door.  But then she gets stuck trying to figure out how to securely communicate to Bob about the dead-drop's location...  She has to have secure communication to initiate secure communication.

Fortunately, Alice is something of a math whiz, and she came up with a solution that works.  

She explained it to me over a beer one night, but most of the details were lost on me.  It's a little hazy, but here's what I remember.

Alice said that she and Bob wanted to pass secret messages to each other.  So here is what Alice came up with:
Alice generates two very large numbers that are mathematically related, but impossible to guess.
Alice keeps one of them to herself <b>(private key)</b>, and posts the other one publicly as her pinned Tweet<b>(public key)</b>.

Bob does the same thing.  
Bob generates two very large numbers that are mathematically related, but impossible to guess.
Bob keeps one of them to himself <b>(private key)</b>, and posts the other one publicly as his pinned Tweet <b>(public key)</b>.

When Bob wants to send a message to Alice, he encrypts his message with <i>Alice's</i> <b>(public key)</b>.  Alice then uses her <b>(private key)</b> to decrypt Bob's message.  It sounded impossible to me, but I tried it out and it seems to work because the public key and the private key are mathematically related somehow.

The same thing happens when Alice wants to send a message to Bob:
When Alice wants to send a message to Bob, she encrypts her message with <i>Bob's</i> <b>(public key)</b>.  Bob then uses his <b>(private key)</b> to decrypt Alice's message.

The whole thing souned crazy to me, so when I got home from the bar that night, I opened up my notebook and tried to figure out how it worked.  Since I'm not the brightest tool in the shed, I decided to use very small numbers.

I think I figured out how Alice and Bob can use the same secret key to encrypt and decrypt their messages, even though they don't know each other's private keys.

Crazy! 

To see how the symmetric key is generated from an asymmetric one, go ahead and run this command:


```python
python alice_bob_message_exchange.py
```

You can run it over and over again, and it works every time.  Here's an example:

```bash
Public key: public_key_base 3, public_key_modulus 23
Alice's private key: 1, shared secret: 1
Bob's private key: 6, shared secret: 1
    Alice's original message: TheBeerRunsAtMidnight
    Alice's encrypted message: UifCffsSvotBuNjeojhiu
    Bob's decryption of Alice's encrypted message: TheBeerRunsAtMidnight
```


Feel free to let your eyes glaze over.  The point is that, through some mathmatical wizardry, both Alice and Bob end up deciding on the same number for the Ceasar Cipher.

If we now run alice_bob_message_exchange.py, we see that an encrypted message can be sent and received, even though both parties have withheld information.



#### Negotiate Encryption
Alice and Bob have shown us how we can use asymmetric keys, along with an agreed upon algorithm, to generate symmetric keys.

The initial connection is asymmetric.  The client encrypts data using the server's public key.  Then, once the client and server agree on a session key (a symmetric key), they can have two-way encrypted communication.

Through some kind of magic, public key cryptography allows two people to share encrypted information even when the encryptor uses a publicly available key.  It sounds strange, but here is how it goes.  In fact, her solution is the basis of secure communication on the internet--the "S" in HTTPS. 




## Challenges

#### Wireshark

    -DNS packet analysis
    -observing the wire (authentication) http://www-net.cs.umass.edu/wireshark-labs/Wireshark_HTTP_v7.0.pdf       http://gaia.cs.umass.edu/wireshark-labs/protected_pages/HTTP-wireshark-file5.html
        -we will learn more about base64 encoding when we talk about JSON Web Tokens



#### Create HTTPS Server
    -Create server
    -Add HTTPS
    -Make your browser trust the cert
    -Create a certificate chain
    https://engineering.circle.com/https-authorized-certs-with-node-js-315e548354a2
    -run a wireshark capture on the loopback, before and after

    chrome://flags/#allow-insecure-localhost


1. You have the outline of a simple node server.  Right now it can handle GET requests ...