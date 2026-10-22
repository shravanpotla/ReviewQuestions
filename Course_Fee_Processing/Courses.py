import csv
from datetime import datetime
from abc import ABC, abstractmethod

with open("courses.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)
valid_rows = []
seen = set()
with open("Error.txt", "w", encoding="utf-8") as error_file:
    for row in data:
        valid = True
        if row["CourseID"] in seen:
            error_file.write(f"Duplicate course ID: {row}\n")
            valid = False
        else:
            seen.add(row["CourseID"])
        if not row["CourseName"].strip():
            error_file.write(f"Invalid course name: {row}\n")
            valid = False

        if row["CourseType"] not in ["Classroom", "Online"]:
            error_file.write(f"Invalid course type: {row}\n")
            valid = False

        try:
            fee = float(row["BaseFee"])
            if fee <= 0:
                error_file.write(f"Invalid base fee: {row}\n")
                valid = False
        except (TypeError, ValueError):
            error_file.write(f"Invalid base fee: {row}\n")
            valid = False

        try:
            discount = float(row["OfferDiscount"])
            if not 0 <= discount <= 100:
                error_file.write(f"Invalid offer discount: {row}\n")
                valid = False
        except (TypeError, ValueError):
            error_file.write(f"Invalid offer discount: {row}\n")
            valid = False

        if row["OfferEndDate"]:
            try:
                datetime.strptime(row["OfferEndDate"], "%Y-%m-%d")
            except (ValueError, TypeError):
                error_file.write(f"Invalid offer date: {row}\n")
                valid = False

        if valid:
            row["BaseFee"] = fee
            row["OfferDiscount"] = discount
            valid_rows.append(row)
        else:
            error_file.write(f"Rejected row: {row}\n")

print("Valid rows:", valid_rows)
print("Total valid rows:", len(valid_rows))


class Course(ABC):
    def __init__(self, course_id, name, fee, discount, end_date):
        self.course_id = course_id
        self.name = name
        self.fee = fee
        self.discount = discount
        self.end_date = end_date

    @abstractmethod
    def fee_calculation(self):
        pass


class ClassroomCourse(Course):
    def fee_calculation(self):
        return self.fee + 2000


class OnlineCourse(Course):
    def fee_calculation(self):
        return self.fee - self.fee * 10 / 100
with open("reports.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "CourseID", "CourseName", "CourseType", "BaseFee",
        "OfferDiscount", "OfferEndDate", "AdjustedFee",
        "OfferStatus", "OfferAmount", "FinalFee"
    ])

    today = datetime.now().date()

    for row in valid_rows:
        course_id = row["CourseID"]
        name = row["CourseName"]
        course_type = row["CourseType"]
        fee = row["BaseFee"]
        discount = row["OfferDiscount"]
        end_date = row["OfferEndDate"]

        if course_type == "Classroom":
            course = ClassroomCourse(
                course_id, name, fee, discount, end_date
            )
        else:
            course = OnlineCourse(
                course_id, name, fee, discount, end_date
            )

        adjusted_fee = course.fee_calculation()
        offer_amount = 0

        if discount > 0 and end_date:
            date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if date > today:
                offer_amount = adjusted_fee * discount / 100

        final_fee = adjusted_fee - offer_amount

        if offer_amount > 0:
            status = "WithOffer"
        else:
            status = "WithoutOffer"

        writer.writerow([
            course_id, name, course_type, fee, discount,
            end_date, adjusted_fee, status, offer_amount, final_fee
        ])

print("Report created successfully.")