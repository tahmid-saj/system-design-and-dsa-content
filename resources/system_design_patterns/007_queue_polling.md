# Queue polling technique

- Sometimes when handling slightly long running requests (between 10 seconds - a few mins), it might be necessary to add some buffer and receive updates on the request status via a message queue and polling. We'll do this since it's not appropriate or feasible to have a hanging GET request for these types of requests, which will take up bandwidth and have unpredictable handle-time.

The workflow is as follows:

1. A traditional message queue, such as with SQS, can be used to enqueue requests when they come into the API servers. The API servers will enqueue requests to the message queue.
2. Additional workers (individual containers / processes) will pull the messages from the queue, then handle the actual request. The request can be: code execution (like with Leetcode), building the binary files (like with a code deployment system), or getting responses from an ML / LLM based chatbot (like with a chatbot system), etc. All of these kinds of use cases which have tasks that may take anywhere from 10 seconds - a few mins can use this approach.
3. While the worker is handling the request, the client can separately poll for any updates from the API servers or a database. Such as the client requesting for updates every 2 secs from a long running request (which might take a bit of time) sent to a traditional LLM / ML model. Let's say the worker (with the chatbot / ML functionality) handling the request updates the database with it's output every 1 sec as it generates the response, then this simple polling approach will also help generate the output on the client side. Depending on the use case, latency requirements, and bandwidth requirements, the polling frequency can be adjusted.
4. Once the worker has handled the request, it can update the database or let the API servers know.

Overall, this simple approach is actually used in multiple apps like Leetcode, code deployment systems, some chatbots, etc, and it improves the user experience by polling for updates, and generating the updates on the client side during this long running request.
