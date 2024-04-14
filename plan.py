#!/usr/bin/python3
import random


def process_data(file_name):
    data = {}
    with open(file_name, "r") as file:
        key = None
        value = ""
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                if key is not None:
                    data[key] = value.strip()
                    value = ""
                key = line[:-1]
            else:
                value += line + "\n"
        if key is not None:
            data[key] = value.strip()
    return data


def is_valid_pair(lunch, dinner):
    valid_pairs = {"A": ["A", "B", "C", "D"], "B": ["A"], "C": ["A"], "D": ["A"]}
    return dinner in valid_pairs.get(lunch, [])


def planMaker(breakfast_data, lunch_data, dinner_data):
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

            if day in [0, 1, 2, 3, 4]:
                spuntino_mattutino = breakfast_data["SPUNTINO"]
            else:
                spuntino_mattutino = ""

            while (breakfast_options, lunch, dinner) in used_options:
                lunch = random.choice(list(lunch_data.keys()))
                dinner_options = [
                    opt
                    for opt in dinner_data.keys()
                    if is_valid_pair(lunch, opt) and opt != lunch
                ]
                if not dinner_options:
                    continue
                dinner = random.choice(dinner_options)

            week_plan.append(
                (
                    breakfast_options,
                    spuntino_mattutino,
                    lunch_data[lunch],
                    lunch_data["SPUNTINO"],
                    dinner_data[dinner],
                )
            )

            used_options.add((breakfast_options, lunch, dinner))

        diet_plan.append(week_plan)
    return diet_plan


def main():
    breakfast = "breakfast.txt"
    lunch = "lunch.txt"
    dinner = "dinner.txt"
    breakfast_data = process_data(breakfast)
    lunch_data = process_data(lunch)
    dinner_data = process_data(dinner)

    diet_plan = planMaker(breakfast_data, lunch_data, dinner_data)

    with open("diet_plan.txt", "w") as output_file:
        output_file.write("Diet plan:\n")
        for i, week in enumerate(diet_plan, 1):
            output_file.write(f"Week {i}:\n")
            for day, meal in enumerate(week, 1):
                output_file.write(f"Day {day}:\n")
                output_file.write(f"Breakfast: \n{meal[0]}\n\n")
                output_file.write(f"Spuntino Mattutino: \n{meal[1]}\n\n")
                output_file.write(f"Lunch: \n{meal[2]}\n\n")
                output_file.write(f"Spuntino Pomeridiano: \n{meal[3]}\n\n")
                output_file.write(f"Dinner: \n{meal[4]}\n\n")
            output_file.write("\n")

    print("Diet plan saved to diet_plan.txt")


if __name__ == "__main__":
    main()
