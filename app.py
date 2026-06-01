import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import warnings
import gdown
warnings.filterwarnings('ignore')

# تنظیمات صفحه
st.set_page_config(
    page_title="پیش‌بینی قیمت مسکن تهران",
    page_icon="🏠",
    layout="wide"
)

# عنوان اصلی
st.title("🏠 پیش‌بینی قیمت مسکن در تهران")
st.markdown("---")

# لیست کامل ایستگاه‌های مترو تهران
metro_stations_complete = [
    (35.8045, 51.4336), (35.7931, 51.4352), (35.7853, 51.4356), (35.7726, 51.4379),
    (35.7626, 51.4440), (35.7600, 51.4337), (35.7565, 51.4257), (35.7482, 51.4273),
    (35.7407, 51.4270), (35.7310, 51.4270), (35.7244, 51.4276), (35.7071, 51.4254),
    (35.7013, 51.4258), (35.6934, 51.4244), (35.6864, 51.4211), (35.6782, 51.4172),
    (35.6730, 51.4165), (35.6677, 51.4154), (35.6575, 51.4141), (35.6506, 51.4162),
    (35.6406, 51.4147), (35.6292, 51.4162), (35.6097, 51.4201), (35.5946, 51.4222),
    (35.5735, 51.3826), (35.5469, 51.3989), (35.5398, 51.3490), (35.5145, 51.3001),
    (35.4161, 51.1522), (35.4890, 50.9239), (35.5450, 51.3730), (35.5215, 51.3692),
    (35.7296, 51.5467), (35.7316, 51.5285), (35.7333, 51.5168), (35.7344, 51.5047),
    (35.7354, 51.4948), (35.7330, 51.4840), (35.7264, 51.4756), (35.7182, 51.4645),
    (35.7091, 51.4534), (35.7021, 51.4457), (35.6993, 51.4377), (35.6922, 51.4329),
    (35.6889, 51.4277), (35.6863, 51.4088), (35.6874, 51.3990), (35.6910, 51.3884),
    (35.6952, 51.3782), (35.7006, 51.3638), (35.7057, 51.3536), (35.7161, 51.3435),
    (35.7175, 51.3309), (35.799759, 51.5216), (35.7979, 51.5081), (35.7959, 51.4935),
    (35.7909, 51.4780), (35.7794, 51.4785), (35.7718, 51.4732), (35.7595, 51.4659),
    (35.7437, 51.4629), (35.7353, 51.4585), (35.7315, 51.4445), (35.7310, 51.4358),
    (35.7283, 51.4174), (35.7216, 51.4088), (35.7009, 51.4058), (35.6810, 51.4015),
    (35.6714, 51.4054), (35.6595, 51.3984), (35.6590, 51.3882), (35.6525, 51.3733),
    (35.6435, 51.3677), (35.6381, 51.3597), (35.6339, 51.3470), (35.6272, 51.3355),
    (35.6989, 51.4985), (35.6926, 51.4886), (35.6913, 51.4777), (35.6913, 51.4677),
    (35.6907, 51.4579), (35.7012, 51.4185), (35.7012, 51.3921), (35.7007, 51.3785),
    (35.7006, 51.3560), (35.7001, 51.3446), (35.7008, 51.3324), (35.6995, 51.3203),
    (35.6906, 51.3196), (35.6886, 51.3271), (35.7055, 51.3074), (35.7308, 51.3068),
    (35.7506, 51.3040), (35.7174, 51.3019), (35.7167, 51.2812), (35.7175, 51.2439),
    (35.7254, 51.1966), (35.7444, 51.1509), (35.7510, 51.0819), (35.7662, 51.0469),
    (35.7870, 51.0026), (35.8009, 50.9647), (35.8248, 50.9330), (35.8261, 50.8881),
    (35.5916, 51.4391), (35.5935, 51.4406), (35.6037, 51.4463), (35.6099, 51.4550),
    (35.6230, 51.4639), (35.6392, 51.4603), (35.6471, 51.4498), (35.6609, 51.4514),
    (35.6728, 51.4478), (35.6809, 51.4491), (35.6861, 51.4480), (35.6903, 51.4472),
    (35.7077, 51.4402), (35.7122, 51.4325), (35.7159, 51.4260), (35.7133, 51.4164),
    (35.7115, 51.4070), (35.7106, 51.3951), (35.7145, 51.3875), (35.7271, 51.3844),
    (35.7305, 51.3660), (35.7348, 51.3525), (35.7401, 51.3402), (35.7483, 51.3287),
    (35.7512, 51.3162), (35.7414, 51.3016), (35.7437, 51.2843), (35.7585, 51.2701),
    (35.7693, 51.2588), (35.7800, 51.2450), (35.6706, 51.5088), (35.6671, 51.4894),
    (35.6681, 51.4769), (35.6742, 51.4654), (35.6717, 51.4358), (35.6683, 51.4248),
    (35.6666, 51.3969), (35.6755, 51.3868), (35.6824, 51.3801), (35.6897, 51.3788),
    (35.7134, 51.3811), (35.7388, 51.3755), (35.7446, 51.3750), (35.7543, 51.3678),
    (35.7653, 51.3600), (35.7777, 51.3493),
]

def min_distance_to_metro(lat, lon):
    distances = [np.sqrt((lat - mlat)**2 + (lon - mlon)**2) for mlat, mlon in metro_stations_complete]
    return min(distances)

# لیست کامل مناطق تهران
mantage_options = [
    'north-shahran', 'bagh-feyz', 'west-shahrak-e-golestan', 'qeytariyeh', 'javadiyeh', 
    'tehranvila', 'darrous', 'tarasht', 'saadat-abad', 'shahrak-e-cheshmeh', 'shahrak-homa',
    'chitgar-lake', 'kooy-e-ferdos', 'south-janat-abad', 'khalij-e-fars', 'shadman', 
    'sazman-barname-jonubi', 'farah-abad', 'shahrak-valiasr-shomali', 'heravi', 'tehransar-markazi',
    'shaharak-e-esteqlal', 'soleymani', 'ostad-moein', 'tehransar-shomali', 'jamalzadeh', 
    'sadeghiyeh', 'jeyhoun', 'haftchenar', 'gomrok', 'jey', 'amaniyeh', 'jordan', 'tavanir',
    'poonak', 'abbas-abad', 'shahr-e-ziba', 'mirdamad', 'sattarkhan', 'kooy-e-bimeh', 'sarsabil',
    'zargandeh', 'west-tehranpars', 'south-shahran', 'bahar', 'majidiyeh', 'dr-hoshyar',
    'university-of-sharif', 'niroo-havayi', 'morvarid-shahr', 'north-sohrevardi', 'aramaneh',
    'selsebil-shomali', 'yousef-abad', 'yakhchi-abad', 'shahid-dastgheyb', 'zafar', 'ekhtiyariyeh',
    'nazi-abad', 'dolatkhah', 'eskandari', 'sepehr', 'sardar-e-jangal', 'vardavard', 'eram',
    'hashemi', 'north-janat-abad', 'marzdaran', 'aboozar', 'north-karegar', 'kuhak', 'sheykh-hadi',
    'almahdi', 'east-tehranpars', 'azad-shahr', 'khaje-nezam-molk', 'narmak', 'central-janat-abad',
    'tohid', 'shahrak-e-gharb', 'taslihat', 'ajoodanieh', 'shahrak-shahid-bagheri', 'khazaneh',
    'elm-o-sanat', 'sazman-ab', 'shams-abad', 'lavizan', 'masoudieh', 'parastar', 'salamat',
    'tehran-gorgan', 'east-shareq', 'azadi-sport-complex', 'ozgol', 'abouzar', 'shirazi',
    'emam-zade-abdollah', 'nabi-akram', 'afsariye-jonubi', 'chitgar-shomali', 'niloufar', 'azari',
    'motahari', 'darya', 'ekbatan', 'pasdaran', 'zafaraniyeh', 'beryanak', 'nosrat',
    'minay-shomali-mokhber', 'hakimiyeh', 'tehran-kerman', 'fallah', 'shahrak-naft-district5',
    'bolvar-e-keshavarz', 'tehran-lashkar', 'makhsous', 'sharara', 'tehran-zanjan', 'shadabad',
    'khaniabad-no-shomali', 'vasfenard', 'yaftabad', 'shahrak-e-kianshahr', 'enqelab', 'ahang',
    'mokhtari', 'sanglaj', 'emamzade-ghasem', 'ghanat-kosar', 'gisha', 'abbasi', 'iranshahr',
    'shahrak-e-taleghani', 'jomhouri', 'tehran-hosein-abad', 'hor-square', 'shahrak-e-vali-e-asr',
    'sahebgharanieh', 'haft-hoz', 'sazamn-barnameh', 'vahidiyeh', 'abshar', 'taxirani', 'tehransar',
    'dezashib', 'moniriyeh', 'sad-dastgah', 'qoba', 'hasan-abad-shomali', 'emam-hossein',
    'amir-bahador', 'shahrak-golha', 'aghdasieh', 'sarsabz', 'andisheh', 'sharif', 'dahom-farvardin',
    'dardasht', 'kan', 'minabi', 'khani-abad', 'eivanak', 'oghaf', 'soleymanieh', 'shahrak-daneshgahi',
    'shahrak-e-parvaz', 'havanirooz', 'tehran-police', 'farmaniyeh', 'seyed-khandan', 'south-mehrabad',
    'shokoofeh', 'behdasht', 'baharestan', 'tehran-jolfa', 'kazem-abad', 'gholhak', 'tehran-no',
    'tehransar-gharbi', 'abshar-tehran', 'niavaran', 'nezam-abad', 'tehran-pars', 'shahid-asadi',
    'shahin', 'chitgar', 'kashanak', 'shahrak-azmayesh-tehran', 'hafezie', 'sohanak', 'imamzadeh-hasan',
    'shamshiri', 'darvazeh-shemiran', 'jaberi', 'aseman', 'parvaz', 'charsad-dastgah', 'sheykh-al-raeis',
    'bashgah-naft', 'habibollah', 'daryan-no', 'saeed-abad', 'shiva', 'behjat-abad', 'bagh-khazaneh',
    'shaharak-e-moslemin', 'doolab', 'helal-ahmar-tehran', 'shahrak-elahiye-gharb', 'elahiyeh',
    'amir-abad', 'imam-sajjad', 'nemat-abad', 'afsariyeh', 'velenjak', 'fadak', 'vanak',
    'shahrak-pasdaran', 'azarbaijan', 'shaharak-e-sharifi', 'motahhari-tehran', 'arjantin',
    'moshiriyeh', 'shahrak-kharazi', 'zehtabi', 'tajrish', 'evin', 'darabad', 'tehran-emamat',
    'south-narmak', 'farzane', 'shahrak-e-jandarmeri', 'qiam', 'amiriyeh', 'gandi', 'azadshahr-tehran',
    'darb-dowom', 'jamaran', 'khavaran', 'chub-tarash', 'majid-abad', 'zarkesh', 'etehad',
    'nejatollahi', 'bahman-yar', 'mahmoodiyeh', 'rah-ahan-tehran', 'tayeb', 'aref', 'zahed-gilani',
    'javadiyeh-tehran-pars', 'shahrak-ati-shahr', 'mina', 'qasemabad', 'dezhkam', 'shahrak-sadeghieh',
    'tolid-daroo', 'shahrak-e-koohsar', 'bolursazi', 'khak-sefid', 'heshamatiyeh', 'varzeshgah-azadi',
    'shahrak-e-takhti', 'jalili', 'dabestan', 'aminhozour', 'valfajr-afsarieh', 'south-ali-abad',
    'simaye-iran', 'peykan-shahr', 'baharan', 'zamzam', 'shaharak-e-shariyati', 'kosar',
    'shahrak-e-ferdows', 'dehqan', 'hekmat', 'golchin', 'shoosh', 'ferdowsi', 'jahad', 'tehran-iran',
    'shahrak-naft', 'shian', 'qezel-qaleh', 'shahrak-e-aboozar', 'dehkade-olympic', 'eshrat-abad',
    'shahrak-e-azadi', 'bisim', 'estakhr', 'qalamestan', 'hesar-booali', 'morad-abad', 'moqadam',
    'shemiran-no', 'molavi', 'chizar', 'harandi', 'kamraniyeh', 'hashem-abad', 'anbar-naft',
    'kooye-e-hefdahom-e-shahrivar', 'niruye-daryaei', 'karevan', 'mazaheri', 'baq-e-azari',
    'khani-abad-no', 'vanak-village', 'valiasr', 'tehran-khaghani', 'eslam-abad', 'farahzad',
    'sarasiab-doolab', 'shahrak-e-mahalati', 'emam-khomeyni-tehran', 'shahrak-mokhaberat',
    'tehran-shandiz', 'arjamandi-rad', 'saheb-al-zaman', 'esfandyari', 'atabak', 'shahid-borujerdi',
    'park-shahr', 'bostan-chitgar', 'sar-asiyab-mehr-abad', 'shahrak-e-darya', 'ebrahim-abad',
    'shahid-fakuri', 'ashtiyani', 'golab-dareh', 'esteghlal', 'darakeh', 'shahrak-e-vilashahr',
    'terminal-gharb', 'ararat', 'bagh-ferdows', 'shahrak-farhangian', 'darband', 'sirous',
    'shahrak-shahrdari', 'shahrak-elm-va-fanavari', 'shokufe-abdol-abad', 'abdol-abad',
    'shahrak-e-apadana', 'negin-gharb', 'tehran-hesarak', 'lalezar', 'shahrak-almahdi-tehran',
    'dolatkhah-shomali', 'hezarsang', 'shahrak-e-omid', 'pamenar', 'shahrak-yas-tehran',
    'shahrak-valfajr', 'shahrak-golha-tehransar', 'shahrak-e-ghazali', 'sorkhe-hesar', 'mahestan',
    'kuy-faraz', 'shahrak-baasat', 'fath', 'shahrak-e-emamkhomeyni', 'shahrak-e-ansar',
    'bostan-velayat', 'mehrabad-airport', 'bazaar', 'meydan-mive-va-terehbar-markazi',
    'shahrak-pardisan-tehran', 'shahrak-booli', 'kuhsar-tehran', 'hassan-abad',
    'namayeshgah-beyn-olmelali', 'shahrak-e-aseman', 'bustan-jangali-lavizan'
]

# لود مدل‌ها از همین پوشه (جایی که app.py قرار داره)
@st.cache_resource
def load_models():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    FILE_ID = "1xl3eADDc1yCEKxQCpg97Ea9vxjTtCopa"  # این رو عوض کن با ID خودت
    
    # لینک دانلود مستقیم (برای فایل‌های بزرگ)
    url = f"https://drive.google.com/uc?id={FILE_ID}&confirm=t"  # confirm=t برای فایل‌های بزرگ [citation:4]
    
    with st.spinner("📥 در حال دانلود مدل (حدود 400MB)..."):
        # دانلود فایل
        gdown.download(url, "RondowmFrest_model_v3.1.pkl", quiet=False)
    FILE_ID = "1fJqy8f8sUrcq0adTGUj8M6fx1oVIrO0Q"  # این رو عوض کن با ID خودت
    
    # لینک دانلود مستقیم (برای فایل‌های بزرگ)
    url = f"https://drive.google.com/uc?id={FILE_ID}&confirm=t"  # confirm=t برای فایل‌های بزرگ [citation:4]
    
    with st.spinner("📥 در حال دانلود مدل (حدود 400MB)..."):
        # دانلود فایل
        gdown.download(url, "xgboost_model_v3.1.pkl", quiet=False)
    xg_filename = "xgboost_model_v3.1.pkl"
    rf_filename = "RondowmFrest_model_v3.1.pkl"
    
    xg_path = os.path.join(current_dir, xg_filename)
    rf_path = os.path.join(current_dir, rf_filename)
    
    xg_model = None
    rf_model = None
    
    # بررسی و لود XGBoost
    if os.path.exists(xg_path):
        try:
            xg_model = joblib.load(xg_path)
            st.success(f"✅ مدل XGBoost با موفقیت لود شد")
        except Exception as e:
            st.error(f"❌ خطا در لود XGBoost: {e}")
    else:
        st.warning(f"⚠️ فایل {xg_filename} در پوشه جاری پیدا نشد")
    
    # بررسی و لود Random Forest
    if os.path.exists(rf_path):
        try:
            rf_model = joblib.load(rf_path)
            st.success(f"✅ مدل Random Forest با موفقیت لود شد")
        except Exception as e:
            st.error(f"❌ خطا در لود Random Forest: {e}")
    else:
        st.warning(f"⚠️ فایل {rf_filename} در پوشه جاری پیدا نشد")
    
    return xg_model, rf_model

# لود مدل‌ها
xg_model, rf_model = load_models()

# بررسی وجود حداقل یک مدل
if xg_model is None and rf_model is None:
    st.error("""
    ❌ **هیچ مدلی یافت نشد!**
    
    لطفاً فایل‌های مدل را در پوشه‌ای که فایل `app.py` قرار دارد کپی کنید.
    
    **مسیر فعلی:** `{}`
    
    **فایل‌های مورد نیاز:**
    - `xgboost_model_v3.1.pkl`
    - `RondowmFrest_model_v3.1.pkl`
    """.format(os.path.dirname(os.path.abspath(__file__))))
    st.stop()

# ستون‌های اطلاعاتی
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 اطلاعات ملک")
    
    mantage = st.selectbox("منطقه/محله", mantage_options, index=mantage_options.index('darvazeh-shemiran') if 'darvazeh-shemiran' in mantage_options else 0)
    metrage = st.number_input("متراژ (متر مربع)", min_value=10, max_value=500, value=84)
    sal = st.slider("سال ساخت", min_value=1360, max_value=1404, value=1394)
    otag = st.selectbox("تعداد اتاق", options=[1, 2, 3, 4, 5, 6], index=1)
    tabage = st.slider("طبقه", min_value=0, max_value=20, value=2)

with col2:
    st.subheader("🏢 امکانات و موقعیت")
    
    vahed_status = st.radio("وضعیت واحد", ["خالی", "پُر"], horizontal=True)
    vahed_status_binary = 0 if vahed_status == "خالی" else 1
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        asansor = st.radio("آسانسور", ["دارد", "ندارد"], horizontal=True)
        asansor_binary = 1 if asansor == "دارد" else 0
    with col_b:
        parking = st.radio("پارکینگ", ["دارد", "ندارد"], horizontal=True)
        parking_binary = 1 if parking == "دارد" else 0
    with col_c:
        anbari = st.radio("انباری", ["دارد", "ندارد"], horizontal=True)
        anbari_binary = 1 if anbari == "دارد" else 0
    
    st.markdown("---")
    lat = st.number_input("عرض جغرافیایی (latitude)", value=35.694974141331, format="%.6f")
    lon = st.number_input("طول جغرافیایی (longitude)", value=51.443905798212, format="%.6f")

# نمایش نقشه تقریبی
st.markdown("---")
st.subheader("🗺️ موقعیت تقریبی ملک")
map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
st.map(map_data, zoom=12)

st.markdown("---")

# دکمه پیش‌بینی
if st.button("🔮 پیش‌بینی قیمت", type="primary", use_container_width=True):
    
    with st.spinner("در حال محاسبه و پیش‌بینی..."):
        
        # محاسبه فاصله تا مترو
        distance_to_metro_raw = min_distance_to_metro(lat, lon)
        distance_to_metro_km = distance_to_metro_raw * 111
        is_near_metro = 1 if distance_to_metro_km < 0.5 else 0
        is_north = 1 if lat > 35.75 else 0
        
        # ساخت دیکشنری با تمام ویژگی‌ها
        all_features = {
            'mantage': mantage,
            'metrage': metrage,
            'sal': sal,
            'otag': otag,
            'tabage': tabage,
            'vahed_status': vahed_status_binary,
            'latitude': lat,
            'longitude': lon,
            'asansor': asansor_binary,
            'parking': parking_binary,
            'anbari': anbari_binary,
            'metrage_log': np.log1p(metrage),
            'building_age': 1404 - sal,
            'building_age_squared': (1404 - sal) ** 2,
            'is_new_building': 1 if (1404 - sal) <= 5 else 0,
            'is_old_building': 1 if (1404 - sal) >= 20 else 0,
            'quality_score': asansor_binary + parking_binary + anbari_binary,
            'has_all_amenities': 1 if (asansor_binary + parking_binary + anbari_binary) == 3 else 0,
            'has_no_amenities': 1 if (asansor_binary + parking_binary + anbari_binary) == 0 else 0,
            'metrage_otag': metrage * otag,
            'metrage_quality': metrage * (asansor_binary + parking_binary + anbari_binary),
            'age_quality': (1404 - sal) * (asansor_binary + parking_binary + anbari_binary),
            'latitude_norm': (lat - 35.7) / 0.05,
            'longitude_norm': (lon - 51.4) / 0.05,
            'otag_per_metrage': otag / metrage if metrage > 0 else 0,
            'floor_ratio': tabage / 10,
            'metrage_rank': 0.5,
            'quality_rank': 0.5,
            'distance_to_metro': distance_to_metro_raw,
            'distance_to_metro_km': distance_to_metro_km,
            'is_near_metro': is_near_metro,
            'is_north': is_north,
            'metrage_original': metrage,
            'sal_original': sal,
            'otag_original': otag,
            'tabage_original': tabage,
            'vahed_status_original': vahed_status_binary,
            'asansor_original': asansor_binary,
            'parking_original': parking_binary,
            'anbari_original': anbari_binary,
            'latitude_original': lat,
            'longitude_original': lon,
            'price_per_m2': 0,
        }
        
        predictions = {}
        
        # پیش‌بینی XGBoost
        if xg_model is not None:
            try:
                # بررسی فیچرهای مورد نیاز مدل XGBoost
                if hasattr(xg_model, 'feature_names_in_'):
                    xg_features = list(xg_model.feature_names_in_)
                    xg_input = {k: v for k, v in all_features.items() if k in xg_features}
                    xg_df = pd.DataFrame([xg_input])
                    xg_df = xg_df[xg_features]
                    pred_log = xg_model.predict(xg_df)[0]
                    pred_price = np.expm1(pred_log)
                    predictions['XGBoost'] = pred_price
                else:
                    # اگه مدل feature_names_in_ نداشت، از همه فیچرها استفاده کن
                    xg_df = pd.DataFrame([all_features])
                    pred_log = xg_model.predict(xg_df)[0]
                    pred_price = np.expm1(pred_log)
                    predictions['XGBoost'] = pred_price
            except Exception as e:
                st.error(f"خطا در پیش‌بینی XGBoost: {e}")
        
        # پیش‌بینی Random Forest
        if rf_model is not None:
            try:
                if hasattr(rf_model, 'feature_names_in_'):
                    rf_features = list(rf_model.feature_names_in_)
                    rf_input = {k: v for k, v in all_features.items() if k in rf_features}
                    rf_df = pd.DataFrame([rf_input])
                    rf_df = rf_df[rf_features]
                    pred_log = rf_model.predict(rf_df)[0]
                    pred_price = np.expm1(pred_log)
                    predictions['Random Forest'] = pred_price
                else:
                    rf_df = pd.DataFrame([all_features])
                    pred_log = rf_model.predict(rf_df)[0]
                    pred_price = np.expm1(pred_log)
                    predictions['Random Forest'] = pred_price
            except Exception as e:
                st.error(f"خطا در پیش‌بینی Random Forest: {e}")
        
        # نمایش نتایج
        if predictions:
            st.balloons()
            
            # نمایش اطلاعات فاصله تا مترو
            st.info(f"🚇 فاصله تا نزدیک‌ترین ایستگاه مترو: {distance_to_metro_km:.2f} کیلومتر | {'✅ نزدیک به مترو (کمتر از 500 متر)' if is_near_metro else '❌ دور از مترو'}")
            
            # کارت اصلی قیمت
            st.markdown("## 💰 نتیجه پیش‌بینی قیمت")
            
            # نمایش میانگین قیمت
            avg_price = np.mean(list(predictions.values()))
            
            col_avg1, col_avg2, col_avg3 = st.columns([1, 2, 1])
            with col_avg2:
                st.markdown(f"""
                <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px;">
                    <h3 style="color: white;">🏠 قیمت میانگین</h3>
                    <h1 style="color: white; font-size: 48px;">{avg_price:,.0f}</h1>
                    <p style="color: white; font-size: 20px;">تومان</p>
                    <p style="color: #ffd700; font-size: 24px;">💰 {avg_price/1_000_000:,.0f} میلیون تومان</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # نمایش قیمت هر مدل
            st.subheader("📊 پیش‌بینی هر مدل")
            
            col_r1, col_r2 = st.columns(2)
            
            for i, (model_name, price) in enumerate(predictions.items()):
                price_per_m2 = price / metrage
                
                if model_name == 'XGBoost':
                    with col_r1:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 10px;">
                            <h3 style="color: white; text-align: center;">🔮 {model_name}</h3>
                            <h2 style="color: white; text-align: center;">{price:,.0f}</h2>
                            <p style="color: white; text-align: center;">تومان</p>
                            <hr style="border-color: white;">
                            <p style="color: white; text-align: center;">💰 {price/1_000_000:,.0f} میلیون تومان</p>
                            <p style="color: #ffd700; text-align: center;">💵 {price_per_m2:,.0f} تومان/متر</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    with col_r2:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 15px; border-radius: 10px;">
                            <h3 style="color: white; text-align: center;">🌲 {model_name}</h3>
                            <h2 style="color: white; text-align: center;">{price:,.0f}</h2>
                            <p style="color: white; text-align: center;">تومان</p>
                            <hr style="border-color: white;">
                            <p style="color: white; text-align: center;">💰 {price/1_000_000:,.0f} میلیون تومان</p>
                            <p style="color: #ffd700; text-align: center;">💵 {price_per_m2:,.0f} تومان/متر</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # بازه قیمتی
            st.subheader("📈 بازه قیمتی تخمینی")
            
            error_percent = st.slider("درصد خطای مجاز:", min_value=5, max_value=30, value=15, step=5)
            
            lower_bound = avg_price * (1 - error_percent/100)
            upper_bound = avg_price * (1 + error_percent/100)
            
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 20px; border-radius: 10px;">
                <p style="text-align: center; font-size: 16px;">بازه قیمتی با {error_percent}% خطا</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="text-align: center;">
                        <p style="color: #666; margin: 0;">حداقل</p>
                        <h3 style="color: #dc3545; margin: 0;">{lower_bound:,.0f}</h3>
                        <small>تومان</small>
                    </div>
                    <div style="flex: 1; margin: 0 20px;">
                        <div style="background: linear-gradient(90deg, #dc3545, #28a745); height: 10px; border-radius: 5px;"></div>
                    </div>
                    <div style="text-align: center;">
                        <p style="color: #666; margin: 0;">حداکثر</p>
                        <h3 style="color: #28a745; margin: 0;">{upper_bound:,.0f}</h3>
                        <small>تومان</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # نمایش قیمت هر متر
            st.markdown("---")
            st.subheader("💵 قیمت هر متر مربع")
            
            cols = st.columns(len(predictions))
            for idx, (model_name, price) in enumerate(predictions.items()):
                with cols[idx]:
                    st.metric(f"{model_name}", f"{price/metrage:,.0f}", "تومان/متر")
            
        else:
            st.error("❌ پیش‌بینی انجام نشد! لطفاً مدل‌ها را بررسی کنید.")

# توضیحات و راهنما
with st.expander("ℹ️ راهنما و توضیحات"):
    st.markdown("""
    ### 📌 نحوه استفاده:
    1. اطلاعات ملک خود را در فرم وارد کنید
    2. روی دکمه "پیش‌بینی قیمت" کلیک کنید
    3. نتایج شامل:
       - قیمت پیش‌بینی شده توسط XGBoost
       - قیمت پیش‌بینی شده توسط Random Forest
       - میانگین قیمت
       - بازه قیمتی با درصد خطای دلخواه
       - قیمت هر متر مربع
    
    ### 🔍 نکات مهم:
    - **فاصله تا مترو** از 150+ ایستگاه محاسبه می‌شود
    - دقت پیش‌بینی به کیفیت اطلاعات بستگی دارد
    - می‌توانید درصد خطای مجاز را تغییر دهید
    
    ### 🏢 فیلدهای ورودی:
    - **منطقه/محله**: موقعیت ملک در تهران
    - **متراژ**: مساحت به متر مربع
    - **سال ساخت**: سال ساخت ساختمان (۱۳۶۰ تا ۱۴۰۴)
    - **تعداد اتاق**: تعداد اتاق‌های خواب
    - **طبقه**: طبقه ملک
    - **امکانات**: آسانسور، پارکینگ، انباری
    - **مختصات**: موقعیت جغرافیایی
    """)

st.markdown("---")
st.caption("🤖 سیستم پیش‌بینی قیمت مسکن تهران | مجهز به XGBoost و Random Forest | محاسبه دقیق فاصله تا مترو")