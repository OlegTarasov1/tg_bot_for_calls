from schemas.fsm_schemas.individual_call_setup import IndividualCallState


async def get_new_state(
    states: dict
) -> list:
    
    list_not_figured = [i for i in states if states.get(i) is None]

    return list_not_figured

