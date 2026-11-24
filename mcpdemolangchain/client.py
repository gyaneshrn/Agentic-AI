from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt.create_react_agent import create_react_agent

from langchain.agents import create_agent

from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()


import asyncio


async def main():
    client=MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args":  ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }  
    )

    import os
    os.environ["GROK_FREE_TEIR"]= os.getenv("GROK_FREE_TEIR")

    tools= await client.get_tools()
    model=ChatGroq(model="qwen/qwen3.8-27b")
    agent= create_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role":"user",  "content": "What's the (3+5) x 12" }]}
    )


    math_response = await agent.ainvoke(
        {"messages": [{"role":"user",  "content": "What's the weather of new york2" }]}
    )

    print("Math response", math_response["messages"][-1].content)


asyncio.run(main())