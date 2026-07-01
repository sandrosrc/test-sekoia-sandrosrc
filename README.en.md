# Technical Test for Sekoia.io - Alexandre Chaillet

## Time spent: 2h

## Environment
- Local Ubuntu
- Docker
- K3d
- DockerHub: https://hub.docker.com/repositories/sandrosrc
- GitHub: https://github.com/sandrosrc/test-sekoia-sandrosrc

## 1 - Setting up a Redis instance

The .aof file was in the old Redis format, so I had to set up a Redis instance with backward compatibility. The file was corrupted with a loss of 100 bytes, which turned out to be a single line from the first stanza. To fix it, I set up a dedicated initContainer that fetches the file from my GitHub repo, then runs an aof check and repairs it directly.

The stack for step 1 is a single pod with 2 initContainers (one to fetch the file, one to fix it if needed), followed by the Redis container itself, exposed through a dedicated Service. That Service isn't actually used in step 1, but I need it in step 3 to expose Redis to the rest of the cluster.

Everything runs as root, which is a potential problem security-wise if this were to go further than a test.

Room for improvement: looking back, I should have used a StatefulSet instead of a naked pod. During step 3, my Redis pod suddenly died, and since it wasn't managed by any controller, it never got recreated automatically. That said, the instructions asked for a single .yaml file, so I stuck with a plain pod.

## 2 - Retrieving the poem, decrypting it, then rewriting it

To find the key needed to decrypt the file, I had to run a DNS dig on a domain that was hardcoded in the .aof file. Once I had the key, I just needed a Python script to decrypt each value and sort them properly before displaying them.

I didn't know Python had a Redis library, so connecting to my Redis instance cost me a bit of time at first. It ended up being pretty handy for the rest of the exercise though.

The script connects to Redis, dynamically fetches all the keys present (rather than hardcoding how many there are), sorts them by name prefix (title / author / inspiration.lineN / verses.stanzaN.lineM), decrypts each one with a repeating-key XOR, and exports the result as YAML.

The "inspiration.line1" key is corrupted, a side effect of the file repair in step 1. Rather than letting the script fail, I replace the non-decodable characters with U+FFFD (the little diamond-shaped question mark).

## 3 - Displaying one stanza per minute with Kubernetes

For the last step, I needed a complete stack that reuses part of what I built earlier. Starting from a Python script that fetches and decrypts the poem, the goal this time was to display a random stanza every minute.

To make this work, I wrote a Dockerfile and pushed the resulting image to my DockerHub (https://hub.docker.com/repository/docker/sandrosrc/poem-display). It spins up a Python environment and installs the dependencies I need, namely the redis library listed in requirements.txt.

That image is then pulled by a CronJob manifest that declares a job called "poem-display", running every minute and printing a random stanza to its logs.

As mentioned above, my Redis pod died partway through this step, which only confirmed that a StatefulSet with a persistent volume would have been the safer choice.

To avoid dependency headaches and keep the whole thing self-contained, the .aof file is pulled directly from a public repo (https://raw.githubusercontent.com/sandrosrc/test-sekoia-sandrosrc/master/poem-1-.aof), and the image itself is public on DockerHub as well (https://hub.docker.com/repository/docker/sandrosrc/poem-display).
