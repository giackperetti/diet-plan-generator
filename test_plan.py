#!/usr/bin/python3
import random


def process_data(file_name):
    meals_data = {}
    snacks_data = {}
    with open(file_name, "r") as file:
        key = None
        value = ""
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                if key is not None:
                    if "SPUNTINO" in key:
                        snacks_data[key] = value.strip()
                    else:
                        meals_data[key] = value.strip()
                    value = ""
                key = line[:-1]
            else:
                value += line + "\n"
        if key is not None:
            if "SPUNTINO" in key:
                snacks_data[key] = value.strip()
            else:
                meals_data[key] = value.strip()
    return meals_data, snacks_data


def is_valid_pair(lunch, dinner):
    valid_pairs = {"A": ["A", "B", "C", "D"], "B": ["A"], "C": ["A"], "D": ["A"]}
    return dinner in valid_pairs.get(lunch, [])


def planMaker(breakfast_data, lunch_data, dinner_data, snacks_data):
    diet_plan = []
    for week in range(4):
        week_plan = []
        used_options = set()
        for day in range(7):
            lunch = random.choice(list(lunch_data.keys()))
            dinner_options = [
                opt
                for opt in dinner_data.keys()
                if is_valid_pair(lunch, opt) and opt != lunch
            ]
            if not dinner_options:
                continue
            dinner = random.choice(dinner_options)

            if day in [5, 6]:  # Saturday and Sunday
                breakfast_options = breakfast_data["A"]
            elif day in [1, 2, 4]:  # Tuesday, Wednesday, Friday
                breakfast_options = breakfast_data["B"]
            else:  # Monday, Thursday
                breakfast_options = breakfast_data["C"]

            spuntino_options = random.choice(list(snacks_data.values()))

            while (breakfast_options, lunch, dinner, spuntino_options) in used_options:
                lunch = random.choice(list(lunch_data.keys()))
                dinner_options = [
                    opt
                    for opt in dinner_data.keys()
                    if is_valid_pair(lunch, opt) and opt != lunch
                ]
                if not dinner_options:
                    continue
                dinner = random.choice(dinner_options)

                if day in [5, 6]:  # Saturday and Sunday
                    breakfast_options = breakfast_data["A"]
                elif day in [1, 2, 4]:  # Tuesday, Wednesday, Friday
                    breakfast_options = breakfast_data["B"]
                else:  # Monday, Thursday
                    breakfast_options = breakfast_data["C"]

                spuntino_options = random.choice(list(snacks_data.values()))

            week_plan.append(
                (
                    breakfast_options,
                    lunch_data[lunch],
                    dinner_data[dinner],
                    spuntino_options,
                )
            )

            used_options.add((breakfast_options, lunch, dinner, spuntino_options))

        diet_plan.append(week_plan)
    return diet_plan


def main():
    lunch = "lunch.txt"
    dinner = "dinner.txt"
    breakfast = "breakfast.txt"
    lunch_data, lunch_snacks = process_data(lunch)
    dinner_data, dinner_snacks = process_data(dinner)
    breakfast_data, breakfast_snacks = process_data(breakfast)

    diet_plan = planMaker(breakfast_data, lunch_data, dinner_data, lunch_snacks)
    # print("Generated diet plan:")
    # for i, week in enumerate(diet_plan, 1):
    #     print(f"Week {i}:")
    #     for day, meal in enumerate(week, 1):
    #         print(f"Day {day}:")
    #         print(f"Breakfast: \n{meal[0]}\n")
    #         print(f"Lunch: \n{meal[1]}\n")
    #         print(f"Dinner: \n{meal[2]}\n")
    #         print("\n")
    #     print("\n")
    with open("diet_plan.txt", "w") as output_file:
        output_file.write("Diet plan:\n")
        for i, week in enumerate(diet_plan, 1):
            output_file.write(f"Week {i}:\n")
            for day, meal in enumerate(week, 1):
                output_file.write(f"Day {day}:\n")
                output_file.write(f"Breakfast: \n{meal[0]}\n\n")
                output_file.write(f"Lunch: \n{meal[1]}\n\n")
                output_file.write(f"Dinner: \n{meal[2]}\n\n")
                output_file.write(f"Snack: \n{meal[3]}\n\n")
            output_file.write("\n")

    print("Diet plan saved to diet_plan.txt")


if __name__ == "__main__":
    main()
