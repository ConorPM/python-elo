import result_processor


def process_result_from_variables(game, user, opponent, user_score, opponent_score):
    # desired format = chess me you 2 0
    rp = result_processor.ResultProcessor(game, user, opponent, user_score, opponent_score)
    rp.get_and_set_result()


def main():
    return


if __name__ == "__main__":
    main()
