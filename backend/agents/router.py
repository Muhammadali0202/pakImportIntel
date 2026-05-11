class AgentRouter:
    def route(self, query: str, context: dict = None) -> str:
        """
        Simple keyword-based router to classify intent.
        Returns the name of the agent to use.
        """
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ["duty", "tax", "tariff", "calculate", "cost", "hscode", "hs code"]):
            return "duty_agent"
        elif any(keyword in query_lower for keyword in ["tracking", "status", "where", "eta", "location", "shipment", "vessel"]):
            return "chat_agent"
        elif any(keyword in query_lower for keyword in ["route", "freight", "air vs sea", "transit time", "air freight", "sea freight", "corridor"]):
            return "route_agent"
        else:
            return "document_agent"
