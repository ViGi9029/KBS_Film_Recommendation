import json
import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to load JSON data from file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

file_path1 = 'dataFilm.json'
file_path2 = 'historyUser.json'
file_path3 = 'preferensiUser.json'

# Load data from JSON files
film_data = load_json(file_path1)
user_history_data = load_json(file_path2)
user_preference_data = load_json(file_path3)

def rekomendasikan_film(orang=None, jumlah=5):
    watched_movies = [item["film"] for item in user_history_data.get(orang, [])] if orang else []
    remaining_movies = [film for film in film_data if film["film"] not in watched_movies]
    recommended_movies = sorted(remaining_movies, key=lambda x: x["rating"], reverse=True)[:jumlah]
    return recommended_movies

def rekomendasikan_film_tahun(orang=None, jumlah=5, tahun=None, bahasa=None, negara=None):
    watched_movies = [item["film"] for item in user_history_data.get(orang, [])] if orang else []
    remaining_movies = [film for film in film_data if film["film"] not in watched_movies]
    if tahun:
        remaining_movies = [film for film in remaining_movies if film["tahun"] == tahun]
    if bahasa:
        remaining_movies = [film for film in remaining_movies if film["bahasa"].lower() == bahasa]
    if negara:
        remaining_movies = [film for film in remaining_movies if film["negara"].lower() == negara]
    recommended_movies = sorted(remaining_movies, key=lambda x: x["rating"], reverse=True)[:jumlah]
    return recommended_movies

def rekomendasikan_film_preferensi(orang=None, jumlah=5):
    preferensi = user_preference_data.get(orang, {}) if orang else {}
    watched_movies = [item["film"] for item in user_history_data.get(orang, [])] if orang else []
    if not preferensi:
        remaining_movies = [film for film in film_data if film["film"] not in watched_movies]
    else:
        remaining_movies = [
            film for film in film_data 
            if film["film"] not in watched_movies
            and film["genre"] in preferensi.get("genre_suka", [])
            and film["tahun"] in preferensi.get("tahun_keluar", [])
            and film["negara"] in preferensi.get("negara_asal", [])
            and film["rating"] >= preferensi.get("rating_minimal", 0)
            and film["usia"] in preferensi.get("target_penonton", [])
        ]
    recommended_movies = sorted(remaining_movies, key=lambda x: x["rating"], reverse=True)[:jumlah]
    return recommended_movies

def bahasa_recommendation(bahasa=None, rating_minimal=0, rating_maksimal=10, jumlah=3):
    recommended_movies = [
        film for film in film_data 
        if (bahasa is None or film["bahasa"].lower() == bahasa)
        and rating_minimal <= film["rating"] <= rating_maksimal
    ]
    recommended_movies = sorted(recommended_movies, key=lambda x: x["rating"], reverse=True)[:jumlah]
    return recommended_movies

def bahasa_recommendation2(bahasa=None, negara=None, jumlah=3):
    recommended_movies = [
        film for film in film_data 
        if (bahasa is None or film["bahasa"].lower() == bahasa) 
        and (negara is None or film["negara"].lower() == negara)
    ]
    recommended_movies = sorted(recommended_movies, key=lambda x: x["rating"], reverse=True)[:jumlah]
    return recommended_movies

def rekomendasikan_film_tahun_bahasa_negara(tahun=None, bahasa=None, negara=None, rating_minimal=0, rating_maksimal=10, jumlah=5):
    filtered_movies = [
        film for film in film_data
        if (tahun is None or film["tahun"] == tahun)
        and (bahasa is None or film["bahasa"].lower() == bahasa)
        and (negara is None or film["negara"].lower() == negara)
        and rating_minimal <= film["rating"] <= rating_maksimal
    ]
    recommended_movies = sorted(filtered_movies, key=lambda x: x["rating"], reverse=True)[:jumlah]
    return recommended_movies

def search_film(film_name):
    for film_info in film_data:
        if film_info["film"].lower() == film_name.lower():
            return film_info
    return None

def main_menu():
    root = tk.Tk()
    root.title("Rekomendasi Film")

    def show_rekomendasi_bahasa():
        bahasa = simpledialog.askstring("Input", "Masukkan bahasa film yang ingin Anda cari rekomendasi: ").lower()
        rating_minimal = simpledialog.askfloat("Input", "Masukkan rating minimal yang diinginkan: ")
        rating_maksimal = simpledialog.askfloat("Input", "Masukkan rating maksimal yang diinginkan: ")

        rekomendasi = bahasa_recommendation(bahasa, rating_minimal, rating_maksimal)
        show_rekomendasi(rekomendasi, f"Rekomendasi Film dalam Bahasa {bahasa.capitalize()} dengan rating antara {rating_minimal} dan {rating_maksimal}:")

    def show_rekomendasi_tahun():
        tahun = simpledialog.askstring("Input", "Masukkan tahun film yang ingin Anda cari rekomendasi (opsional): ")
        bahasa = simpledialog.askstring("Input", "Masukkan bahasa film yang ingin Anda cari rekomendasi (opsional): ").lower()
        negara = simpledialog.askstring("Input", "Masukkan negara asal film yang diinginkan (opsional): ").lower()
        rating_minimal = simpledialog.askfloat("Input", "Masukkan rating minimal yang diinginkan: ")
        rating_maksimal = simpledialog.askfloat("Input", "Masukkan rating maksimal yang diinginkan: ")

        tahun = int(tahun) if tahun else None
        bahasa = bahasa if bahasa else None
        negara = negara if negara else None

        rekomendasi = rekomendasikan_film_tahun_bahasa_negara(tahun=tahun, bahasa=bahasa, negara=negara, rating_minimal=rating_minimal, rating_maksimal=rating_maksimal)
        show_rekomendasi(rekomendasi, f"Rekomendasi Film berdasarkan kriteria yang Anda berikan:")

    def show_rekomendasi_preferensi():
        user = simpledialog.askstring("Input", "Masukkan nama pengguna untuk mendapatkan rekomendasi berdasarkan preferensi: ").lower()
        rekomendasi = rekomendasikan_film_preferensi(user)
        show_rekomendasi(rekomendasi, f"Rekomendasi Film untuk pengguna {user}:")

    def show_rekomendasi_bahasa_negara():
        bahasa = simpledialog.askstring("Input", "Masukkan bahasa film yang ingin Anda cari rekomendasi: ")
        negara = simpledialog.askstring("Input", "Masukkan negara asal film yang diinginkan: ")

        # Jika input bahasa atau negara kosong atau None, set menjadi None
        bahasa = bahasa.lower() if bahasa else None
        negara = negara.lower() if negara else None

        rekomendasi = bahasa_recommendation2(bahasa, negara)
        result = f"Rekomendasi Film {'dalam Bahasa ' + bahasa.capitalize() if bahasa else ''} {'dari Negara ' + negara.capitalize() if negara else ''}:\n"
        for movie in rekomendasi:
            result += f"Judul: {movie['film']}, Rating: {movie['rating']}, Tahun: {movie['tahun']}, Negara: {movie['negara']}\n"

        messagebox.showinfo("Hasil Rekomendasi", result)
    
        jawab = simpledialog.askstring("Input", "Apakah Anda ingin mencari top 5 film berdasarkan tahun tertentu? (ya/tidak) ").lower()
        if jawab == "ya":
            tahun = simpledialog.askinteger("Input", "Masukkan tahun film yang ingin Anda cari rekomendasi (misalnya 2020): ")
            rekomendasi_tahun = rekomendasikan_film_tahun("alex", jumlah=5, tahun=tahun, bahasa=bahasa, negara=negara)
            result = f"Rekomendasi top 5 film untuk tahun {tahun} {'dalam Bahasa ' + bahasa.capitalize() if bahasa else ''} {'dari Negara ' + negara.capitalize() if negara else ''}:\n"
            for movie in rekomendasi_tahun:
                result += f"Judul: {movie['film']}, Rating: {movie['rating']}, Tahun: {movie['tahun']}, Negara: {movie['negara']}\n"
            messagebox.showinfo("Hasil Rekomendasi", result)

        search = simpledialog.askstring("Input", "Apakah Anda menemukan film yang ingin Anda cari? (ya/tidak) ").lower()
        if search == "tidak":
            film_name = simpledialog.askstring("Input", "Masukkan film yang ingin Anda cari: ").lower()
            film_info = search_film(film_name)
            if film_info:
                result = "Informasi Film:\n"
                result += f"Judul: {film_info['film']}\n"
                result += f"Rating: {film_info['rating']}\n"
                result += f"Bahasa: {film_info['bahasa']}\n"
                result += f"Tahun: {film_info['tahun']}\n"
                result += f"Target Penonton: {film_info['usia']}\n"
                messagebox.showinfo("Informasi Film", result)
            else:
                messagebox.showinfo("Informasi Film", "Film tidak ditemukan.")


    def show_rekomendasi(rekomendasi, title):
        top = tk.Toplevel(root)
        top.title(title)
        for idx, movie in enumerate(rekomendasi):
            tk.Label(top, text=f"Judul: {movie['film']}, Rating: {movie['rating']}, Tahun: {movie['tahun']}, Negara: {movie['negara']}").pack()
        tk.Button(top, text="Kembali ke menu utama", command=top.destroy).pack()

    tk.Button(root, text="Rekomendasi berdasarkan bahasa", command=show_rekomendasi_bahasa).pack()
    tk.Button(root, text="Rekomendasi berdasarkan tahun", command=show_rekomendasi_tahun).pack()
    tk.Button(root, text="Rekomendasi berdasarkan preferensi pengguna", command=show_rekomendasi_preferensi).pack()
    tk.Button(root, text="Rekomendasi berdasarkan bahasa dan negara", command=show_rekomendasi_bahasa_negara).pack()
    tk.Button(root, text="Keluar", command=root.quit).pack()

    root.mainloop()

if __name__ == "__main__":
    main_menu()
