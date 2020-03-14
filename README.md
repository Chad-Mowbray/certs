# HTTPS, Certificates, and Packet Sniffing
Today you are going to see for yourself what separates HTTP from HTTPS.

## Public Key Cryptography
You might have noticed that, when browsing on the internet, you will occasionally see different icons to the left of the url bar.

If we go to some random [blog](http://derpturkey.com/), we see an information icon with "Not secure" text.

![not secure](readme/derpturkey.png)

If we click on the icon, we get some scary red text reiterating that our connection is indeed not secure. 

![scary red text](readme/scary-red.png)

But don't unplug your computer and hide under the bed just yet.  That warning is just telling you that the website's server is using HTTP.  HTTP just means that the traffic is unencrypted and could be intercepted without any real effort (as we'll see shortly).  

In this case, I think the attempt to scare you away from derpturkey.com is a little overblown.  After all, it's just a blog.  You go there, you read the content, and then you leave.  <i>You</i> aren't sending any data, and you certainly aren't sending any sensitive data--at least not on purpose.  However, if you are going to be sending data that you wouldn't want the whole world to see, then you should encrypt your data before you send it--with HTTPS.

So why not just always use HTTPS?  Well, some people think that you <i>should</i> always use HTTPS. But it does make things more complicated.  Is it worth the trouble for derpturkey.com?  After today's challenges you'll be better placed to weigh the pros and cons based on the use case.

Browser makers are among those who would prefer that you always use HTTPS (hence the dramatic warnings). And things are trending in that direction anyway.  Most major sites now use HTTPS--and the percentage is likely to continue rising.  So even if you aren't sending and receiving sensitive information, you are more likely than not, using encryption.

And encryption is the real difference between HTTP and HTTPS.  Before we get into how all of this works, let's try intercepting some traffic from both an HTTP and an HTTPS connection to see what all the fuss is about.

### Introduction to Wireshark
In order to intercept all that traffic, we are going to use a very common networking tool called Wireshark.  You can download Wireshark for free [here](https://www.wireshark.org/download.html).

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

The higher the numbers go, the further we get from wires and switches.  We spend most of our time at the very top of the OSI model, but it's not a bad idea to know a little bit about the lower layers.

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

Now let's do the same with with a server that uses HTTPS, owasp.org:

![tcp-tls](readme/tls-owasp.png)

To find what we're looking for, we can either just scan the resulting packets ourselves, or play around with the filters.  

If we wanted to filter our results by IP address, we would first need to find owasp.org's IP address:
```bash
curl owasp.org -v
```
Then we apply the filter:
```bash
ip.addr == ipv6.src == 2601:240:c400:8660:f451:8c51:19cd:9c88 or ipv6.dst == 2601:240:c400:8660:f451:8c51:19cd:9c88
```
When we compare these results to our earlier HTTP capture, we find a several differences.  First off, the protocols are different.  Instead of HTTP, we have TLS, which you can think of as encrypted HTTP or HTTPS.  What other differences do you notice? 
    
(port, encrypted application data is gibberish, more packets, etc)

![tcp-stream](readme/encrypted-application-data-owasp.png)

Here we have no idea what information we were sending to the server.  So even if someone had intercepted this, they wouldn't be able to do anything with it. If I were giving someone my credit card information, this is how I'd want to do it.

There's a whole lot more than just this.  For example, we can also take a look at the "certificate" that the owasp.org server sent to us:

![owasp-certificate](readme/certificate-owasp.png)

And we can take a more detailed view, where we can see a few tidbits of information:

![cert-detail](readme/cert-detail-owasp.png)

### Certificates
OK, so now we know that HTTP is unencrypted and HTTPS is encrypted.  But how does this encryption happen?  The long answer is long, but the short answer is: certificates.  

It's pretty easy to get your hands on a certificate--at least to look at.  Just go to any page that uses HTTPS:

```bash
duckduckgo.com
```

If we click on the "lock" icon to the left of the url bar, instead of being jolted by scary red text, we are soothed with a reassuring green:

![valid certificate](readme/valid-cert.png)

We can continue to find out more if we click on the certificate. The certificate actually has quite a bit of information in it. Take a quick look, but don't bother trying to understand everything now.

Why does it look like duckduckgo.com has three certificates?

It turns out that duckduckgo.com's certificate doesn't just contain information about itself, but also information about the certificate (DigiCert SHA2 Secure Server CA) that is vouching for duckduckgo.com's certificate.

And if we do the same thing with DigiCert SHA2 Secure Server CA's certificate, we find that it was issued by DigiCert Global Root CA.  

Wait, so the same company, DigiCert is issuing certificates to itself?  There's actually a good reason for that.  You'll learn more when you do today's challenges.  It turns out that the entire system of credibility that undergirds encrytption on the internet is just a small group of big companies saying that they trust each other--so you can trust who they trust.  Yikes!

But it seems to be working for the moment.  Those top level players are called Certificate Authorities, and all roads lead to them.

The chain of certificates that starts with duckduckgo.com leads up to one of the elect Certificate Authorities, in this case DigiCert Global Root CA.  

So why should I trust DigiCert Global Root CA, I've never even heard of them?

It turns out that you don't have to, because your browser or operating system trusts them for you. Go to your settings in Google Chrome and search for "Manage Certificates".  Eventually you should be able to see all of the certificates from the Certificate Authorities:

![Root CAs](readme/root-ca.png)

Yes, you've had all these certificates the whole time!  

### Generating Certificates
In fact there is a command line utility that allows us to generate our own certificates all day long.  Try it!

```bash
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
```

Congratulations, you've just generated a public key and a private key that can be used to encrypt communication on the web!  The problem is that this is a "self-signed" certificate--outside the web of trust spun by the Certificate Authorities.  It still works though.  In fact DigiCert Global Root CA probably ran the same command to generate their own root certificate--they just did it in an underground bunker somwhere in Nevada.


### Back to HTTPS
Now that we know a little bit about the mechanism that enables trust on the internet, let's get back to our packets.

We saw some TCP packets that preceeded either the HTTP or TLS protocols.  HTTPS adds some extra steps to the initial interaction between a client (browser) and a server. Before sending the application data (OSI layer 7), there is what is called a "TLS handshake".  The TLS handshake is where the encryption is negotiated.

![TLS Handshake](readme/tls_handshake.png)

The end result of all these steps is an agreement between the client and the browser to use a specific encryption mechanism.  So when you send your credit card number in a form, even if someone intercepts the message (very easy to do  we've seen), there won't be anything useful for a potential attacker to steal.

#### The TLS Handshake
We are going to present a somewhat simplified overview of that negotiation--called the TLS handshake.

1. The Server Sends the Certificate to the Client
2. The Client Authenticates the Certificate
3. The Client and Server Negotiate Encryption

##### The Server Sends the Certificate to the Client
Before any application data is sent (i.e. the webpage), an encrypted session needs to be established between the client and the server.  The server is the responsible party here.  It is the server's duty to establish trustworthiness.  

In order to do that, as we've already seen, the server sends along its certificate to establish its identity.  A certificate is basically just a filled out form that is meant to prove that the server is who it says it is.

##### The Client Authenticates the Certificate
As we've seen, what the server sends the client isn't just it's own certificate (called a "leaf", because it is at the end of the "branch"), but a <b>chain</b> of certificates.  The client then checks that the chain leading from the server's leaf certificate all the way up to the Certificate Authority is valid.  That Certificate Authority's root certificate is stored in your browser and/or operating system.

It must ensure that the chain matches, the certificates are not expired, and the certificates have not been revoked.  

It is worth noting here that a valid certificate only establishes the <i>identity</i> of the certificate holder, not moral uprightness.  It's like checking a salesman's driver's licence.  At least it's something.

If the certificate checks out, and the client (browser) trusts that the server is who it says it is, then the client and server can agree on encryption.

The process of negotiating encryption is fairly complicated, so before we talk about the third step, let's try to understand a simplified example.  

## Ceasar Cipher Example
Let's imagine two secret agents, Alice and Bob.  They live far away from each other, but need to communicate securely.  So they agree to encrypt their letters using a Caesar Cipher--pretty clever.  Anyone who intercepts their letters will just see gibberish.  

But there is a problem.

If Alice wants to exchange encrypted letters with Bob using a Ceasar Cipher, they both need to have the same secret key to encode/decode the letter (for example, the number "17").  In other words, they need a "symmetric" key.  But how can Alice tell Bob what the secret key is?  If she simply writes the key in the top corner of the letter, anyone who intercepts the letter will be able to decode it.  

A real conundrum, but there might be a way around it.  Alice thinks about establishing a dead-drop that only she and Bob both know about, where she can write the secret key in chalk above a certain door.  But then she gets stuck trying to figure out how to securely communicate to Bob about the dead-drop's location...  She has uncovered a fundamental problem in securing symmetrically encrypted communications:  how to begin?

She needs to have secure communication to initiate secure communication.

Fortunately, Alice is something of a math whiz, and she came up with a solution that works.  

She explained it to me over a beer one night, but frankly, most of the details were over my head.  It's a little hazy, but here's what I remember.

Alice said that she and Bob wanted to pass secret messages to each other, but needed a way to start the process without having a shared secret (symmetric key).  So naturally, she said, why not use an "asymmetric" key?  An asymmetric approach allows both parties to have their own private key, and a second public key that anyone can see.

She then implemented her asymmetic key idea by generating two very large numbers that are mathematically related, but (effectively) impossible to guess.

Alice keeps one of them to herself <b>(private key)</b>, and posts the other one publicly as her pinned Tweet<b>(public key)</b> so that anyone, including Bob, can see it.

Bob does the same thing.  He generates two very large numbers that are mathematically related, but impossible to guess. Bob keeps one of them to himself <b>(private key)</b>, and posts the other one publicly as his pinned Tweet <b>(public key)</b>.

When Bob wants to send a message to Alice, he encrypts his message with <i>Alice's</i> <b>(public key)</b>.  Alice then uses her <b>(private key)</b> to decrypt Bob's message.  It sounded impossible to me, but I tried it out and it seems to work because the public key and the private key are mathematically related somehow.

The same thing happens when Alice wants to send a message to Bob:
When Alice wants to send a message to Bob, she encrypts her message with <i>Bob's</i> <b>(public key)</b>.  Bob then uses his <b>(private key)</b> to decrypt Alice's message.

The whole thing souned crazy to me, so when I got home from the bar that night, I opened up my notebook and tried to figure out how it worked.  Since I'm not the brightest tool in the shed, I decided to use very small numbers.

I think I figured out how Alice and Bob can generate a symmetric key seemingly out of thin air--even though they don't know each other's private keys.

I saved my notebook in a folder called "bob_alice".  To see how the symmetric key is generated from an asymmetric one, go ahead and run this command from inside it:

```python
python alice_bob_message_exchange.py
```
You can run it over and over again, and it works every time.  Here's an example:

```bash
Public key: public_key_base 3, public_key_modulus 23
Alice's private key: 4, shared secret: 9
Bob's private key: 6, shared secret: 9
    Alice's original message: TheBeerRunsAtMidnight
    Alice's encrypted message: CqnKnnaAdwbJcVrmwrpqc
    Bob's decryption of Alice's encrypted message: TheBeerRunsAtMidnight
```

It's OK, I don't understand it either.  The point is that, through some mathmatical wizardry, both Alice and Bob end up deciding on the same symmetric key for their Ceasar Cipher encryption--even though both parties have withheld information from the other.

#### The Client and Server Negotiate Encryption
What Alice discovered is called Public Key Cryptography. It is a system that allowed her and Bob to bootstrap a secure communication session.
HTTPS (TLS) <i>starts out</i> using asymmetric keys, but then generates symmetric keys to use for the rest of the session.

When you generated the public/private key pair earler using the openssl command line utility, you enabled yourself to bootstrap a secure communication session with someone.  That is the basis of secure communication on the internet.

## Challenges

### Wireshark--Password Sniffing
<b>Note: This exercise works best if you use an incognito window</b>

We're going to borrow an exercise from a UMass computer science class to show you the dangers of sending sensitive information over unencrypted HTTP.  Go ahead and start up a Wireshark capture.

Then, go to the following site: 

http://gaia.cs.umass.edu/wireshark-labs/protected_pages/HTTP-wireshark-file5.html

There you can enter the following credentials:

&nbsp;&nbsp;&nbsp;&nbsp;username: wireshark-students<br>
&nbsp;&nbsp;&nbsp;&nbsp;password: network

![wireshark-ex1](readme/wireshark-ex1.png)

You should see the TCP and HTTP packets.  Take a look at them.  Can you find your credentials anywhere in the Hypertext Transfer Protocol?

##### <span style="color: red;">Solution: Authorization: Basic d2lyZXNoYXJrLXN0dWRlbnRzOm5ldHdvcms=</span> 

It might take you a minute, since they don't look quite the way you'd expect.  You might even think they were encrypted... But hold on, didn't I just tell you that you were sending your credentials unencrypted over HTTP?  Well it turns out that your credentials aren't actually encrypted--they're just <i>encoded</i>.  Do some searching, find out what encoding is used, and then decode your credentials.  What do you see?

##### <span style="color: red;">Solution: base64 encoding, wireshark-students:network</span> 

### Create an HTTPS Server
##### Part I
The first challenge showed you first hand what can happen when you send credentials in the clear.  Instead of just complaining about the problem, we should fix it.

We are going to create a simple server that allows people to submit a username and password, just like in the Wireshark exercise.  The server has already been started, but you need to add the POST endpoint and display a message of some kind.

Once you get that going, you can test out your wire sniffing skills (on loopback) yet again to make sure that you see where the credentials are going.

##### <span style="color: red;">Solution:</span> 
![password](readme/password-ex1.png)

##### Part II
<b>Note: For this one you need to tell Chrome to relax.  chrome://flags/#allow-insecure-localhost</b>

So far so good.  Now we are going to fix things.  Instead of an HTTP server, we are going to make an HTTPS server.  In order to do that you'll need to get yourself a certificate (a public/private key pair).  I think there was a command for doing just that somewhere in the lesson.

Once you get it working, unleash your wire sniffer and see if you can capture the credentials.  

##### <span style="color: red;">Solution:</span> 
![password-tls](readme/wireshark-ex3.png)


### Bonus
1. Your browser still doesn't trust your certificate.  Can you make it?

##### <span style="color: red;">Solution:</span> 
(add to Trusted Root Certification Authorities store)

2. Imagne yourself as the newest Certificate Authority.  You wouldn't want to directly sign a website's certificate.  If anything went wrong you might invalidate your root certificate.  To mitigate your risk, create an intermediate certificate that can do the dirty work of signing a website's certificate.

##### <span style="color: red;">Solution:</span> 
https://raymii.org/s/tutorials/OpenSSL_command_line_Root_and_Intermediate_CA_including_OCSP_CRL%20and_revocation.html


