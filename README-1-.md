# Interview test for Sekoia.io Infrastructure Team

The goal of this quick test is to validate your ability to work with basic principles used by the infrastructure team.
It should take you about one hour.
The deliverables is a tar archive that you will have to send us back.
The exercise is organized in successive steps, that must be completed in order.

## Pre-requisite

You will need :
- `kubectl`
- a kubernetes instance (k3s, k3d, minikube, a managed cloud instance ...)
- a docker registry (docker hub, ghcr.io, quay.io ...)
- a way to build & push docker images
- a way to write and test a small Python script

## Description of the exercise

A very important poem has been written by an almighty SRE and you have been chosen to receive it (```poem.aof``` / hash sha256 : ```733f971d7f1bb31214ef5db40754c8451b8739b4a3316af3ce72412809617f73```)
The poem is stored in an encrypted format in a AOF file (from a Redis instance), and your goal is to retrieve it and share its content to the world.

Please note that this file has been stored for hundreds of years now and might be slightly damaged !

## 1. Redis instance

Write a kubernetes stack that downloads the AOF file and correctly loads it into a Redis database.

Result expected:
- a single YAML file

## 2. Poem retrieval

Write a python script that connects to the Redis instance and decodes the poem.
Beware ! The poem is split into parts and encrypted with a secret key.
Our cryptographers found the algorithm used is a basic XOR, but they are not sure where the key is, you'll have to find it *somewhere*. However, they know that the key ends with an exclamation mark.

Result expected:
- a single Python3 file (+ requirements.txt if needed)
- the whole poem, as a valid YAML file

## 3. Spread the good word

Now you should have retrieved the poem in all its beauty. It's time to share it !

Write a kubernetes stack and python script that displays a random stanza of the poem, every minute.

Result expected:
- a single Python3 file (+ requirements.txt if needed)
- a buildable Dockerfile
- a single YAML file (Kubernetes stack) that logs random stanza of the poem, every minute, using the docker image you just created

## Sharing your result

Results should be shared in a tar.gz archive. Please group the results in 3 folders named `1` / `2` / `3`, corresponding to each step of the exercise.
At the same level, include a global README.md file that documents important points and difficulties you encountered, as well as the time spent on the exercise. Nothing more is strictly expected in that README, we would just like to see what you think is important to document here, considering you solved (or not !) a puzzle. It is a documentation exercise.

If you think that is relevant, you can also include information about how you set up your environment for the exercise.

If you are stuck, don't hesitate to reach out to the person that sent you the exercise.

### A note about dependencies

Ensure that your submission is entirely self-contained and does not rely on any pre-existing components or environment-specific settings. The Python scripts and Kubernetes stacks should work out-of-the-box on a fresh Kubernetes instance.
