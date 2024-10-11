
def score_count(result: str, global_score: dict) -> str:
    if "True" in result:
        global_score["total_score"] += 10
        global_score["exercises_completed"] += 1
        print(f'Good answer, your score is now  : {
              global_score["total_score"]} / 100.')
    else:
        print(f"Wrong answer, your score is : {
              global_score['total_score']} / 100.")


def has_been_evaluated():
    pass


def mark_as_evaluated():
    pass
