
def assign_risk_category(probability):

    if probability >= 0.75:
        return "Critical"

    if probability >= 0.50:
        return "High"

    if probability >= 0.25:
        return "Moderate"

    return "Low"


def assign_retention_priority(probability):

    if probability >= 0.80:
        return "Immediate Action"

    if probability >= 0.60:
        return "High Priority"

    if probability >= 0.40:
        return "Monitor"

    return "Low Priority"


def get_risk_message(risk_category):

    messages = {
        "Critical": (
            "This customer requires immediate "
            "retention intervention."
        ),
        "High": (
            "This customer should receive proactive "
            "retention support."
        ),
        "Moderate": (
            "Monitor this customer and consider "
            "targeted engagement."
        ),
        "Low": (
            "This customer currently demonstrates "
            "a relatively stable profile."
        )
    }

    return messages[risk_category]
