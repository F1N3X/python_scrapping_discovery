import matplotlib.pyplot as plt
import csv
import os

def circular_diagram_by_category(csv_files_folder):
    categories = []
    book_counts = []

    for csv_file in os.listdir(csv_files_folder):
        if csv_file.endswith('.csv'):
            category_name = csv_file.replace('.csv', '')
            categories.append(category_name)

            csv_file_path = os.path.join(csv_files_folder, csv_file)
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = sum(1 for _ in reader)
                book_counts.append(count)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9,11))

    ax1.pie(book_counts, startangle=90, colors=plt.cm.Paired.colors)
    ax1.set_title('Répartition du nombre de livres par catégorie')
    ax1.axis('equal') 

    table_data = [[cat, count] for cat, count in zip(categories, book_counts)]
    column_labels = ["Catégorie", "Nombre de livres"]
    ax2.axis('tight')
    ax2.axis('off')
    table = ax2.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    plt.show()

circular_diagram_by_category('csv_files')



def calculate_average_prices_and_plot_histogram(csv_files_folder):
    categories = []
    average_prices = []

    for csv_file in os.listdir(csv_files_folder):
        if csv_file.endswith('.csv'):
            category_name = csv_file.replace('.csv', '')
            categories.append(category_name)

            total_price = 0
            count = 0

            csv_file_path = os.path.join(csv_files_folder, csv_file)
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    price = row['price_including_tax'].replace('£', '').strip()
                    total_price += float(price)
                    count += 1

            average_price = total_price / count if count > 0 else 0
            average_prices.append(average_price)

    plt.figure(figsize=(10, 6))
    plt.bar(categories, average_prices, color='skyblue')
    plt.title('Moyenne des prix des livres par catégorie')
    plt.xlabel('Catégorie')
    plt.ylabel('Prix moyen (£)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.show()

calculate_average_prices_and_plot_histogram('csv_files')