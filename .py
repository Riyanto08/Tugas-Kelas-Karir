import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

product_df = pd.read_csv('product.csv')
region_df = pd.read_csv('region.csv')
reseller_df = pd.read_csv('reseller.csv')
sales_df = pd.read_csv('sales.csv')
sales_person_df = pd.read_csv('sales_person.csv')
sales_person_region_df = pd.read_csv('sales_person_region.csv')
target_df = pd.read_csv('target.csv')

#Menggabungkan sales_df dengan product_df menggunakan product_key
sales_product_df = pd.merge(sales_df, product_df, on='product_key', how='left')

#Menggabungkan hasil dengan region_df menggunakan sales_teritory_key
sales_product_region_df = pd.merge(sales_product_df, region_df, left_on='sales_teritory_key', right_on='sales_teritory_key', how='left')

# Bersihkan kolom pada dataset sales
sales_product_region_df['unit_price'] = sales_product_region_df['unit_price'].replace('[\$,]', '', regex=True).astype(float)
sales_product_region_df['sales'] = sales_product_region_df['sales'].replace('[\$,]', '', regex=True).astype(float)
sales_product_region_df['cost'] = sales_product_region_df['cost'].replace('[\$,]', '', regex=True).astype(float)
sales_product_region_df['standard_cost'] = sales_product_region_df['standard_cost'].replace('[\$,]', '', regex=True).astype(float)
# Konversi kolom order_date menjadi datetime
sales_product_region_df['order_date'] = pd.to_datetime(sales_product_region_df['order_date'])

# Tambahkan kolom profit
sales_product_region_df['profit'] = sales_product_region_df['sales'] - sales_product_region_df['cost']

# Buat kolom kuartal
sales_product_region_df['quarter'] = sales_product_region_df['order_date'].dt.to_period('Q')

# Hitung total profit per kuartal
profit_per_quarter = sales_product_region_df.groupby('quarter')['profit'].sum().reset_index()

# Buat barplot
plt.figure(figsize=(12, 6))
sns.barplot(x='quarter', y='profit', data=profit_per_quarter, palette='viridis')

# Buat barplot
plt.figure(figsize=(12, 6))
sns.barplot(x='quarter', y='profit', data=profit_per_quarter, palette='viridis')

# Tambahkan label dan judul
plt.title('Total Profit Per Quarter', fontsize=16)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Total Profit', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Tampilkan grafik
plt.show()

# Buat kolom perubahan profit
profit_per_quarter['profit_change'] = profit_per_quarter['profit'].diff()

# Buat kolom persentase perubahan profit
profit_per_quarter['profit_change_pct'] = (profit_per_quarter['profit_change'] / 
                                           profit_per_quarter['profit'].shift(1)) * 100

# Tampilkan hasil
print(profit_per_quarter)

# Ganti nilai NaN di 'profit_change' dan 'profit_change_pct' dengan 0
profit_per_quarter['profit_change'] = profit_per_quarter['profit_change'].fillna(0)
profit_per_quarter['profit_change_pct'] = profit_per_quarter['profit_change_pct'].fillna(0)

# Pastikan kolom 'quarter' dalam format string
profit_per_quarter['quarter'] = profit_per_quarter['quarter'].astype(str)

# Debug nilai di 'profit_change' dan 'profit_change_pct'
print(profit_per_quarter[['profit_change', 'profit_change_pct']].head())

# Konversi kolom 'profit_change' dan 'profit_change_pct' ke tipe numerik
profit_per_quarter['profit_change'] = pd.to_numeric(profit_per_quarter['profit_change'], errors='coerce')
profit_per_quarter['profit_change_pct'] = pd.to_numeric(profit_per_quarter['profit_change_pct'], errors='coerce')

# Plot lineplot
plt.figure(figsize=(14, 7))

# Plot perubahan profit
sns.lineplot(x='quarter', y='profit_change', data=profit_per_quarter, marker='o', label='Profit Change', color='blue')

# Plot persentase perubahan profit
sns.lineplot(x='quarter', y='profit_change_pct', data=profit_per_quarter, marker='o', label='Profit Change (%)', color='green')

# Tambahkan label dan judul
plt.title('Profit Change and Percentage Change Per Quarter', fontsize=16)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Change', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Metrics')
plt.axhline(0, color='red', linestyle='--', linewidth=0.8)  # Garis nol untuk referensi
plt.tight_layout()

# Tampilkan grafik
plt.show()

# Kelompokkan data berdasarkan kuartal dan kategori, lalu hitung total profit
profit_per_category = sales_product_region_df.groupby(['quarter', 'category'])['profit'].sum().reset_index()

# Pivot table untuk format lebih rapi (kuartal sebagai index, kategori sebagai kolom)
profit_per_category_pivot = profit_per_category.pivot_table(index='quarter', columns='category', values='profit', fill_value=0)

# Tampilkan hasil
print(profit_per_category_pivot)

# Buat barplot untuk total profit per kategori produk secara kuartal
profit_per_category_pivot.plot(kind='bar', figsize=(14, 7))

# Tambahkan judul dan label
plt.title('Total Profit per Category per Quarter', fontsize=16)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Total Profit', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Tampilkan grafik
plt.show()

# Kelompokkan data berdasarkan kuartal dan kategori, lalu hitung total sales
sales_per_category = sales_product_region_df.groupby(['quarter', 'category'])['sales'].sum().reset_index()

# Pivot table untuk format lebih rapi (kuartal sebagai index, kategori sebagai kolom)
sales_per_category_pivot = sales_per_category.pivot_table(index='quarter', columns='category', values='sales', fill_value=0)

# Tampilkan hasil
print(sales_per_category_pivot)

# Buat barplot untuk total sales per kategori produk secara kuartal
sales_per_category_pivot.plot(kind='bar', figsize=(14, 7), colormap='viridis')

# Tambahkan judul dan label
plt.title('Total Sales per Category per Quarter', fontsize=16)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Tampilkan grafik
plt.show()

# Kelompokkan data berdasarkan kuartal dan kategori, lalu hitung total cost
cost_per_category = sales_product_region_df.groupby(['quarter', 'category'])['cost'].sum().reset_index()

# Pivot table untuk format lebih rapi (kuartal sebagai index, kategori sebagai kolom)
cost_per_category_pivot = cost_per_category.pivot_table(index='quarter', columns='category', values='cost', fill_value=0)

# Tampilkan hasil
print(cost_per_category_pivot)

# Buat barplot untuk total cost per kategori produk secara kuartal
cost_per_category_pivot.plot(kind='bar', figsize=(14, 7), colormap='plasma')

# Tambahkan judul dan label
plt.title('Total Cost per Category per Quarter', fontsize=16)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Total Cost', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Tampilkan grafik
plt.show()

