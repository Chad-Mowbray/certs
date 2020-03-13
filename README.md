# HTTPS, Certificates, and Packet Sniffing
Today we are going to go over what separates HTTP from HTTPS and why you should care.

## Public Key Cryptography
You might have noticed that, when browsing on the internet, you will occasionally see different icons to the left of the url bar.

If we go to some random [blog](http://derpturkey.com/), we see an information icon with "Not secure" text.

![not secure](readme/derpturkey.png)

If we click on the icon, we get some scary red text reiterating that our connection is indeed not secure. 

![scary red text](readme/scary-red.png)

But don't unplug your computer and hide under the bed just yet.  That warning is just telling you that the website's server is using HTTP.  HTTP just means that the traffic is unencrypted and could be intercepted without any real effort (as we'll see shortly).  

In this case, I think the attempt to scare you away from derpturkey.com is a little overblown.  After all, it's just a blog.  You go there, you read the content, and then you leave.  <i>You</i> aren't sending any data, and you certainly aren't sending any sensitive date.  However, if you are going to be sending data that you wouldn't want the whole world to see, then you should encrypt your data before you send it--with HTTPS.

So why not just always use HTTPS?  Well, some people think that you <i>should</i> always use HTTPS. But it does make things more complicated.  Is it worth the trouble for derpturkey.com?  After today's challenges you'll be better placed to weigh the pros and cons based on the use case.

Browser makers are among those who would prefer that you always use HTTPS (hence the dramatic warnings). And things are trending in that direction anyway.  Most major sites now use HTTPS--and the percentage is likely to continue rising.  So even if you aren't sending and receiving sensitive information, you are more likely than not, using encryption.

And encryption is the real difference between HTTP and HTTPS.  Before we get into how all of this works, let's try intercepting some traffic from both an HTTP and an HTTPS connection to see what all the fuss is about.

### Introduction to Wireshark
In order to intercept all that traffic, we are going to use a very common networking tool called Wireshark.  You can download it for free [here](https://www.wireshark.org/download.html).

Hopefully, after using Wireshark, you'll be just a little bit more paranoid about web security.  Let's just let it run for a minute and see what we get:

(run capture)

Depending on what you were doing, you probably got quite a bit more than you were expecting.  All that output can be overwhelming, but we don't worry.  We're going to walk through a few important points.

Instead of just capturing everything, let's focus in on one particular website using a filter.  We will look at derpturkey.com, a random Javascript coding blog.  We'll first get the ip address so that we can filter our network capture:

```bash
curl derpturkey.com -v
```
If you look at the first couple lines of output, you will see derpturkey.com's ip address: 50.16.86.72.  We can paste this into the filter bar:

```bash
ip.addr == 50.16.86.72
```
![HTTP capture](readme/derpturkey-http-capture.png)

Now try clicking around the webpage and and watch what happens in the Wireshark window.  You should see clumps of packets start to populate your screen.  

If you look at the "protocol" columnn, you will notice that some are TCP and others are HTTP--and that TCP preceeds HTTP.  If you double-click on one of the packets, you'll get a popup window.  In the top pane of the window, you have five lines.  Each one of those lines is a "layer" in the network.  They go from low-level to high-level.  The first line is the lowest layer, and the last is HTTP.  

These layers bring us to the so-called "OSI model". The OSI (Open Systems Interconnection) model is an abstraction that is used to understand the different layers in a network-- all the way from wires to cat pictures.

The OSI model has either 7 or 5 layers, depending on who you ask (5,6,and 7 are sometimes collapsed together).  And for our purposes, 5 is fine.  


![osi](readme/tcp-ip-stack.png)
<!-- https://docs.oracle.com/cd/E19683-01/806-4075/ipov-10/index.html

![OSI](readme/OSI.PNG) -->

The higher the numbers go, the more abstract things get.  We spend most of our time at the very top of the OSI model, but it's not a bad idea to know a little bit about the lower layers.

Wireshark gives a good illustration of the 5-layer OSI model:

![wireshark-osi](readme/http-wireshark.png)

2. Datalink (Ethernet II)
3. Network (Internet Protocol Version 4)
4. Transport (Transmission Control Protocol)
5. Application (Hypertext Transfer Protocol)

We already know a little something about the Network layer (IP)--it's where we got our address (50.16.86.72), and we'll be playing around with the Transport layer too (TCP)

Feel free to click around, but for now we only care about the Application layer.  

If you expand the Hypertext Transfer Protocol line, you should see some familiar faces.  The kind of request (GET), the different headers, and so on.

In the bottom window we have the raw bytes on the left, and the slightly-easier-to-read utf-8 encoding on the right.  These are the chunks that make up the flow of the internet.

Wireshark also allows us to take a look at an entire conversation.  Choose a packet, right-click it, then follow, then HTTP stream.  You should see the whole conversation laid out for you.  

![http-conversation](readme/http-conversation.png)

This packet capture represents the detailed history of our internet session.  It's a good thing we didn't send anything important over the wire!

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

Here you'll notice a couple differences.  First off, the protocols are different.  Instead of HTTP, we have TLS, which you can think of as encrypted HTTP or HTTPS.  What other differences do you notice? 
    -port, encrypted application data is gibberish

![tcp-stream](readme/tcp-stream.png)

Here we have no idea what information we were sending to the server.  So even if someone had intercepted this, they wouldn't be able to do anything with it. If I were giving someone my credit card information, this is how I'd want to do it.

### Certificates
OK, so now we know that HTTP is unencrypted and HTTPS is encrypted.  But how does this encryption happen?  The long answer is long, but the short answer is: certificates.  

It's pretty easy to get your hand on a certificate--at least to look at.  Just go to any page that uses HTTPS:

```bash
duckduckgo.com
```

If we click on the "lock" icon to the left of the url bar, instead of being jolted by scary red text, we are soothed with a reassuring green:

![valid certificate](readme/valid-cert.png)

We can continue to find out more if we click on the certificate. The certificate actually has quite a bit of information in it. Take a quick look, but don't bother trying to understand everything now.

Why does it look like duckduckgo.com has three certificates?

It turns out the duckduckgo.com's certificate doesn't just contain information about itself, but also information about the certificate (DigiCert SHA2 Secure Server CA) that is vouching for duckduckgo.com's certificate.

And if we do the same thing with DigiCert SHA2 Secure Server CA's certificate, we find that it was issued by DigiCert Global Root CA.  

Wait, so the same company, DigiCert is issuing certificates to itself?  There's actually a good reason for that.  You'll learn more when you do today's challenges.  It turns out that the entire system of credibility that undergirds encrytption on the internet is just a small group of big companies saying that they trust each other--so you can trust who they trust.  Yikes!

But it seems to be working for the moment.  Those top level players are called Certificate Authorities, and all roads lead to them.

The chain of certificates that starts with duckduckgo.com leads up to one of the elect Certificate Authorities, in this case DigiCert Global Root CA.  

So why should I trust DigiCert Global Root CA, I've never even heard of them?

It turns out that you don't have to, because your browser or operating system trusts them for you. Go to you settings in Google Chrome and search for "Manage Certificates".  Eventually you should be able to see all of the certificates from the Certificate Authorities:

![Root CAs](readme/root-ca.png)

Yes, you've had all these certificates the whole time.  Later on, you'll see what happens when that certificate chain has a broken link, and what you might be able to do to fix it.

### Back to HTTPS
Now that we know a little bit about the mechanism that enables trust on the internet, let's get back to our packets.

We saw some TCP packets that preceeded either the HTTP or TLS protocols.  HTTPS adds some extra steps to the initial interaction between a client (browser) and a server. Before sending the application data (OSI layer 7), there is what is called a "TLS handshake".  The TLS handshake is when the encryption is negotiated.

![TLS Handshake](readme/tls_handshake.png)

The end result of all these steps is an agreement between the client and the browser to use a specific encryption mechanism.  So when you send your credit card number in a form, even if someone intercepts the message (very easy to do  we've seen), there won't be anything useful for a potential attacker to steal.

#### The TLS Handshake
We are going to present a somewhat simplified overview of that negotiation--called the TLS handshake.

// https://www.thesslstore.com/blog/explaining-ssl-handshake/

1. The Server Sends the Certificate to the Client
2. The Client Authenticates the Certificate
3. Negotiate Encryption

#### The Server Sends the Certificate to the Client
Before any application data is sent (i.e. the webpage), an encrypted session needs to be established between the client and the server.  The server is the responsible party here.  It is the server's duty to establish trustworthiness.  

In order to do that, as we've already seen, the server sends along its certificate to establish its identity.  A certificate is basically just a filled out form that is meant to prove that the server is who it says it is.

#### The Client Authenticates the Certificate
As we've seen, what the server sends the client isn't just it's own certificate (called a "leaf", because it is at the end of the "branch"), but a <b>chain</b> of certificates.  The client then checks that the chain leading from the server's leaf certificate all the way up to the Certificate Authority is valid.  That Certificate Authority's root certificate is stored in your browser and/or operating system.

It must ensure that the chain matches, the certificates are not expired, and the certificates have not been revoked.  

It is worth noting here that a valid certificate only establishes the <i>identity</i> of the certificate holder, not moral uprightness.  It's like checking a salesman's driver's licence.  At least it's something.

If the certificate checks out, and the client (browser) trusts that the server is who it says it is, then the client and server can agree on encryption.

The process of negotiating encryption is fairly complicated, so let's look at a simplified example.  

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
What Alice discovered is called Public Key Cryptography. It is a system that allowed her and Bob to bootstrap secure communication.
HTTPS uses asymmetric keys, along with an agreed upon algorithm, to generate symmetric keys.

In fact there is a command line utility that allows us to generate certificates all day long.  Try it!

```bash
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
```

You've just generated a public key and a private key that can be used to encrypt communication.  The problem is that this is a "self-signed" certificate--outside the web of trust spun by the Certificate Authorities.  It still works though.


The initial connection is asymmetric.  The client encrypts data using the server's public key.  Then, once the client and server agree on a session key (a symmetric key), they can have two-way encrypted communication.

Through some kind of magic, public key cryptography allows two people to share encrypted information even when the encryptor uses a publicly available key.  It sounds strange, but here is how it goes.  In fact, her solution is the basis of secure communication on the internet--the "S" in HTTPS. 



## Challenges

#### Wireshark--Password Sniffing
<b>Note: This exercise works best if you use an incognito window</b>

We're going to borrow an exercise from a UMass computer science class to show you the dangers of sending sensitive information over unencrypted HTTP.  Go ahead and start up a Wireshark capture.

Then, go to the following site: 

http://gaia.cs.umass.edu/wireshark-labs/protected_pages/HTTP-wireshark-file5.html

There you can enter the following credentials:

&nbsp;&nbsp;&nbsp;&nbsp;username: wireshark-students<br>
&nbsp;&nbsp;&nbsp;&nbsp;password: network

![wireshark-ex1](readme/wireshark-ex1.png)

You should see the TCP and HTTP packets.  Take a look at them.  Can you find your credentials anywhere in the Hypertext Transfer Protocol?

### <span style="color: red;">Solution: Authorization: Basic d2lyZXNoYXJrLXN0dWRlbnRzOm5ldHdvcms=</span> 

It might take you a minute, since they don't look quite the way you'd expect.  You might even think they were encrypted... But hold on, didn't I just tell you that you were sending your credentials unencrypted over HTTP?  Well it turns out that your credentials aren't actually encrypted--they're just <i>encoded</i>.  Do some searching, find out what encoding is used, and then decode your credentials.  What do you see?

### <span style="color: red;">Solution: base64 encoding, wireshark-students:network</span> 

#### Create HTTPS Server
##### Part I
The first challenge showed you first hand what can happen when you send credentials in the clear.  Instead of just complaining about the problem, we should fix it.

We are going to create a simple server that allows people to submit a username and password, just like in the Wireshark exercise.  The server has already been started, but you need to add the POST endpoint and display a message of some kind.

Once you get that going, you can test out your wire sniffing skills (on loopback) yet again to make sure that you see where the credentials are going.

![password](readme/password-ex1.png)

##### Part II
<b>Note: For this one you need to tell Chrome to relax.  chrome://flags/#allow-insecure-localhost</b>

So far so good.  Now we are going to fix things.  Instead of an HTTP server, we are going to make an HTTPS server.  In order to do that you'll need to get yourself a certificate (a public/private key pair).  I think there was a command for doing just that somewhere in the lesson.

Once you get it working, unleash your wire sniffer and see if you can capture the credentials.  


##### Bonus
Make a certificate chain







    -Create server
    -Add HTTPS
    -Make your browser trust the cert
    -Create a certificate chain
    https://engineering.circle.com/https-authorized-certs-with-node-js-315e548354a2
    -run a wireshark capture on the loopback, before and after

    chrome://flags/#allow-insecure-localhost


1. You have the outline of a simple node server.  Right now it can handle GET requests ...