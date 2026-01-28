import asyncio
import sys
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message

class EchoAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Agent received: {msg.body}")
                reply = msg.make_reply()
                reply.body = f"Echo: {msg.body}"
                await self.send(reply)
    
    async def setup(self):
        print(f"EchoAgent starting at {self.jid}")
        template = Template()
        self.add_behaviour(self.ReceiveBehaviour(), template)

async def main():
    # XMPP server for testing
    agent_jid = "stra_ang3r@xmpp.jp"  
    agent_password = "y12$d34*!#"
    
    agent = EchoAgent(agent_jid, agent_password)
    
    try:
        await agent.start(auto_register=True)
        print("Agent started. Press Ctrl+C to stop.")
        await asyncio.Event().wait()  
    except KeyboardInterrupt:
        print("\nStopping agent...")
    finally:
        await agent.stop()
        print("Agent stopped.")

if __name__ == "__main__":
    asyncio.run(main())