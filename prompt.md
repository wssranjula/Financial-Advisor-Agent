Please build an AI agent for Financial Advisors that integrates with Gmail, Google Calendar and Hubspot. we need to create own o-auth apps and credentials as they are all free
This  must do all of the following:

- I can log in to the app using Google OAuth (request email read/write permissions, calendar read/write permission).
    - Please add [webshookeng@gmail.com](mailto:webshookeng@gmail.com) as an OAuth test user
- I can connect my Hubspot CRM account (Hubspot offers self-serve OAuth app setup and a free testing account)
- The main app interface is a ChatGPT-like chat interface where I can:
    - Ask the agent a question about clients and it uses information from email and Hubspot to answer the question
        - You should use RAG (pgvector, or whatever you want) to import all the emails from gmail and records from hubspot (contacts and contact notes) and use this data as context to answer the question
        - Examples of questions I might ask:
            - Who mentioned their kid plays baseball?
            - Why did greg say he wanted to sell AAPL stock
    - Ask the agent to do things for me
        - It should use tool calling
        - It should store tasks in a database and have memory so that tasks that require waiting for a response can be continued until completion.
        - Examples of requests I might make:
            - “Schedule an appointment with Sara smith”
                - This would look up Sara smith in Hubspot, or previous emails, email her asking to set up an appointment (sharing available times from my calendar), when she responds, take appropriate action (like add to calendar, make a note of the interaction in Hubspot, respond letting them know its done. If they respond saying none of the times work, send some new times. You should rely on the LLM and tool calling to handle edge cases. It should be extremely flexible).
            - I can give it ongoing instructions like “When someone emails me that is not in Hubspot, please create a contact in Hubspot with a note about the email.”
                - The agent should remember ongoing instructions and should consider those instructions when webhooks from either gmail, calendar or Hubspot come in. (or you can use polling)
                - Some more examples of ongoing instructions:
                    - “When I create a contact in Hubspot, send them an email telling them thank you for being a client”
                    - “When I add an event in my calendar, send an email to attendees tell them about the meeting”
                - With this, make the agent somewhat proactive. Prompt it whenever something happens in the 3 integrations (gmail, calendar, Hubspot) to see if it wants to proactively do something with any of the tools available.
                    - This should handle the case where a client emails me asking when our upcoming meeting is and the agent looks it up on the calendar and responds.
                - You should accomplish this using:
                    - memory of general ongoing instructions and RAG
                    - tool calling
                    - I would not hard code these scenarios, I would just test to make sure the AI has the tools necessary to accomplish them
    - Please match these responsive designs for the chat interface ./ui.png

We want to achive this by leveragin langchain DeepAgents framework. 