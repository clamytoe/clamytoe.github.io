title: Troubleshooting Connectivity Issues
date: 2020-08-10 11:11
category: Misc
tags: windows10, icmp, ping, firewall, ftp
slug: troubleshooting-connectivity-issues
author: Martin Uribe
summary: Had issues connecting to FTP server running on Windows 10

# Troubleshooting Connectivity Issues

My son likes to live stream on Youtube and was in the middle of one the other day when his phone ran out of space.
He asked me to backup his images and videos for him so that he could make some room.

## Some Background

I've been an avid Linux user for ages so I've gotten used to not having to use iTunes.
I recently made the move back to Windows 10, but I detest having to use iTunes to do anything on my phone, so I don't even have it installed.

Back when I was on Linux, I had found [FTPManager Pro](https://apps.apple.com/us/app/ftpmanager-pro/id522627917) in the Apple app store, which would allow me to start an FTP server so that I could just use [Filezilla](https://filezilla-project.org/download.php) to upload audio files to my phone as well as allow me to copy my images and videos to my network storage device.

## Attacking the Problem

I thought, no problem.
I already had Filezilla installed, so I fired it up and connected.
Unfortunately, those images and videos did not show up.
FTPManager has its own directory that you can access, but Apple apparently won't allow it to access the rest of the filesystem.

My next thought was to just run an FTP server on my computer, and use FTPManager to transfer the files, because from within the app the media files in question are available; just not to its built-in FTP server.
So I downloaded [Filezilla's FTP server](https://filezilla-project.org/download.php?type=server) utility.
After a quick run through the settings, creating a user and home directory, I fired it up.

Back on the phone, I setup the new server and attempted to connect to it.
No-Go.
The phone kept reporting that the server was not reachable.
I double, tripple-checked all of the settings and everything looked good.
I fired up Filezilla on my computer and connected to localhost on port 21 and I was able to get in!

## The Problem

Back on the phone, I found a way to diagnose connection issues.
Under *Network Diagnostics* it listed the following entries:

* Resolve Host
* Ping Host
* Connect Port

The *Resolve Host* was the IP address that I had entered for my machine.
I opened up a command prompt on one of my kids computers and attempted to ping my machine.
Nothing, 100% packet loss...

So with no connectivity between my phone and my computer and not being able to ping my computer from another computer, it's easy to conclude that the issue is with my computer blocking the traffic.

## Firewall: Custom Rule

I remembered that at work, while setting up some Samba mounts on a Windows machine, I had run into similar problems because the server could not ping the machines.
I had to go into the *Firewall* settings and enable ICMP ping on IPv4, we don't use IPv6 so I didn't see a need to enable it on that protocol.
I found this really good [article](https://www.osradar.com/how-to-enable-and-disable-ping-icmp-in-windows-10-firewall/) on how to do it and was now able to ping my machine in no time.

## Firewall: Program Rule

Although FTPManager could now ping my machine, it still could not connect to the FTP server.
I went back into the Firewall settings and did the same as above for ICMP, but this time instead of creating a new **Custom** command, I selected **Program**.

![program]({static}/images/fw-program.png)

On the **Program** screen, I selected **This program path** and clicked on the _Browse_:

![path]({static}/images/fw-path.png)

From within the **Open** dialog windows, I navigated to where the _Filezilla Server_ was installed and selected it:

![filezilla]({static}/images/fw-filezilla.png)

From the **Action** dialog window, I left it at the default _Allow the connection_:

![action]({static}/images/fw-action.png)

I left the **Profile** page as default:

![profile]({static}/images/fw-profile.png)

I then gave it a generic name and clicked on _Finish_:

![name]({static}/images/fw-name.png)

Here you can see that the new rul is running and is active:

![rule]({static}/images/fw-rule.png)

With that final addition, FTPManager was able to connect and I was able to proceeded with the backing up the media files.

## Conclusion

Don't give up when you run into problems, there's always a way!
