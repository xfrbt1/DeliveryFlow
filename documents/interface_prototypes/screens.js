import React from 'react';
import {
  User, Lock, Mail, MapPin, Package,
  Truck, CheckCircle, ChevronLeft, Search,
  Clock, Plus, Map, Navigation, Phone
} from 'lucide-react';

// Компонент-обертка для имитации экрана мобильного телефона
const PhoneScreen = ({ title, children, showBack = false }) => (
  <div className="w-80 h-[40rem] bg-gray-50 border-8 border-gray-900 rounded-[2.5rem] overflow-hidden flex flex-col relative shadow-2xl shrink-0">
    {/* Header */}
    <div className="bg-white px-4 py-3 flex items-center justify-between border-b shadow-sm z-10">
      <div className="flex items-center gap-2">
        {showBack && <ChevronLeft size={20} className="text-gray-600" />}
        <h1 className="font-bold text-lg text-gray-800">{title}</h1>
      </div>
      <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
        <User size={14} className="text-blue-600" />
      </div>
    </div>

    {/* Content */}
    <div className="flex-1 overflow-y-auto bg-gray-50 relative pb-6">
      {children}
    </div>

    {/* Home indicator */}
    <div className="absolute bottom-2 left-1/2 -translate-x-1/2 w-1/3 h-1 bg-gray-300 rounded-full"></div>
  </div>
);

export default function App() {
  return (
    <div className="min-h-screen bg-gray-200 p-8 flex flex-col items-center">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">CourierFlow — UI Мокапы</h1>
      </div>

      <div className="flex flex-wrap justify-center gap-8 max-w-7xl">

        {/* Экран 1: Регистрация и выбор роли */}
        <PhoneScreen title="Регистрация">
          <div className="p-5 flex flex-col h-full">
            <div className="text-center mb-8 mt-4">
              <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-lg">
                <Package size={32} className="text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800">CourierFlow</h2>
              <p className="text-sm text-gray-500 mt-1">Доставка в один клик</p>
            </div>

            <div className="space-y-4 flex-1">
              <div className="bg-white p-3 rounded-xl border flex items-center gap-3">
                <Mail size={18} className="text-gray-400" />
                <input type="email" placeholder="Email" className="bg-transparent w-full text-sm outline-none" disabled />
              </div>
              <div className="bg-white p-3 rounded-xl border flex items-center gap-3">
                <Lock size={18} className="text-gray-400" />
                <input type="password" placeholder="Пароль" className="bg-transparent w-full text-sm outline-none" disabled />
              </div>

              <div className="mt-6 mb-2">
                <p className="text-sm font-medium text-gray-700 mb-2">Выберите вашу роль:</p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="border-2 border-blue-500 bg-blue-50 rounded-xl p-3 flex flex-col items-center gap-2 cursor-pointer">
                    <User size={24} className="text-blue-600" />
                    <span className="text-sm font-semibold text-blue-700">Клиент</span>
                  </div>
                  <div className="border border-gray-200 bg-white rounded-xl p-3 flex flex-col items-center gap-2 cursor-pointer opacity-70">
                    <Truck size={24} className="text-gray-500" />
                    <span className="text-sm font-medium text-gray-600">Курьер</span>
                  </div>
                </div>
              </div>
            </div>

            <button className="w-full bg-blue-600 text-white font-semibold py-3.5 rounded-xl shadow-md mt-4">
              Зарегистрироваться
            </button>
            <p className="text-center text-xs text-gray-500 mt-4">
              Уже есть аккаунт? <span className="text-blue-600 font-medium">Войти</span>
            </p>
          </div>
        </PhoneScreen>

        {/* Экран 2: Список заказов (Customer) */}
        <PhoneScreen title="Мои заказы">
          <div className="p-4">
            <div className="relative mb-5">
              <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input type="text" placeholder="Поиск по номеру..." className="w-full bg-white border rounded-xl py-2 pl-10 pr-4 text-sm" disabled />
            </div>

            <div className="space-y-4">
              {/* Активный заказ */}
              <div className="bg-white rounded-xl p-4 border shadow-sm relative overflow-hidden">
                <div className="absolute top-0 left-0 w-1 h-full bg-orange-400"></div>
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold text-gray-500">ЗАКАЗ #CF-1024</span>
                  <span className="bg-orange-100 text-orange-700 text-[10px] font-bold px-2 py-1 rounded-md">В ПУТИ</span>
                </div>
                <div className="flex items-center gap-2 mt-3">
                  <div className="flex flex-col items-center">
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                    <div className="w-0.5 h-6 bg-gray-200"></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  </div>
                  <div className="flex flex-col gap-3 text-sm text-gray-700">
                    <p>Ул. Пушкина, 10</p>
                    <p>Пр-т Ленина, 45</p>
                  </div>
                </div>
              </div>

              {/* Завершенный заказ */}
              <div className="bg-white rounded-xl p-4 border shadow-sm relative overflow-hidden opacity-75">
                <div className="absolute top-0 left-0 w-1 h-full bg-green-500"></div>
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold text-gray-500">ЗАКАЗ #CF-1023</span>
                  <span className="bg-green-100 text-green-700 text-[10px] font-bold px-2 py-1 rounded-md">ДОСТАВЛЕН</span>
                </div>
                <div className="flex items-center gap-2 mt-3 text-sm text-gray-600">
                  <CheckCircle size={16} className="text-green-500" />
                  <span>Вчера, 14:30</span>
                </div>
              </div>
            </div>
          </div>

          {/* FAB - Создать заказ */}
          <div className="absolute bottom-6 right-4">
            <div className="w-14 h-14 bg-blue-600 rounded-full shadow-lg flex items-center justify-center text-white cursor-pointer">
              <Plus size={28} />
            </div>
          </div>
        </PhoneScreen>

        {/* Экран 3: Создание заказа (Customer) */}
        <PhoneScreen title="Новый заказ" showBack={true}>
          <div className="p-4 space-y-5">

            <div className="bg-white p-4 rounded-xl border shadow-sm">
              <h3 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <MapPin size={16} className="text-blue-500" />
                Маршрут доставки
              </h3>

              <div className="space-y-3 relative">
                <div className="absolute left-3 top-4 bottom-4 w-0.5 bg-gray-200"></div>

                <div className="relative z-10 flex items-center gap-3">
                  <div className="w-6 h-6 rounded-full bg-gray-100 border border-gray-300 flex items-center justify-center text-[10px] font-bold text-gray-500">A</div>
                  <input type="text" placeholder="Откуда забрать?" className="flex-1 border-b pb-1 text-sm outline-none" value="Ул. Тверская, 1" disabled />
                </div>
                <div className="relative z-10 flex items-center gap-3">
                  <div className="w-6 h-6 rounded-full bg-blue-100 border border-blue-300 flex items-center justify-center text-[10px] font-bold text-blue-600">B</div>
                  <input type="text" placeholder="Куда доставить?" className="flex-1 border-b pb-1 text-sm outline-none" disabled />
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border shadow-sm">
              <h3 className="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <Package size={16} className="text-blue-500" />
                Детали груза
              </h3>
              <textarea
                placeholder="Что везем? (например: документы, коробка 2кг)"
                className="w-full bg-gray-50 border rounded-lg p-3 text-sm h-20 outline-none resize-none"
                disabled
              ></textarea>
            </div>

            <div className="bg-blue-50 p-4 rounded-xl border border-blue-100">
              <p className="text-xs text-blue-800 flex items-center gap-2">
                <Clock size={14} />
                После создания вы получите Tracking URL для отслеживания.
              </p>
            </div>

            <button className="w-full bg-blue-600 text-white font-semibold py-3.5 rounded-xl shadow-md mt-4">
              Оформить заказ
            </button>

          </div>
        </PhoneScreen>

        {/* Экран 4: Биржа заказов (Courier) */}
        <PhoneScreen title="Доступные заказы (Курьер)">
          <div className="p-4">
            <div className="flex gap-2 mb-4">
              <div className="px-3 py-1.5 bg-gray-800 text-white text-xs font-semibold rounded-full">Новые</div>
              <div className="px-3 py-1.5 bg-white border text-gray-600 text-xs font-medium rounded-full">Рядом</div>
            </div>

            <div className="space-y-4">
              <div className="bg-white rounded-xl p-4 border border-blue-200 shadow-sm">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <span className="text-xs font-bold text-gray-500 block">#CF-1025</span>
                    <span className="text-sm font-semibold text-gray-800">Документы</span>
                  </div>
                  <span className="text-xs font-medium text-gray-500 flex items-center gap-1">
                    <Clock size={12} /> 2 мин назад
                  </span>
                </div>

                <div className="flex flex-col gap-2 text-sm text-gray-700 mb-4 bg-gray-50 p-3 rounded-lg border border-dashed">
                  <div className="flex items-start gap-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full mt-1.5"></div>
                    <span className="flex-1 text-xs">ул. Баумана, 12 (Забрать)</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-1.5"></div>
                    <span className="flex-1 text-xs font-medium">ул. Горького, 5 (Доставить)</span>
                  </div>
                </div>

                <button className="w-full bg-green-500 text-white font-bold py-2.5 rounded-lg text-sm shadow-sm hover:bg-green-600">
                  Принять заказ
                </button>
              </div>

              <div className="bg-white rounded-xl p-4 border shadow-sm opacity-80">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <span className="text-xs font-bold text-gray-500 block">#CF-1026</span>
                    <span className="text-sm font-semibold text-gray-800">Коробка (3 кг)</span>
                  </div>
                  <span className="text-xs font-medium text-gray-500">15 мин назад</span>
                </div>
                <div className="flex flex-col gap-2 text-sm text-gray-700 mb-4 bg-gray-50 p-3 rounded-lg">
                  <p className="text-xs truncate">От: ТЦ "Галерея"</p>
                  <p className="text-xs truncate">До: ЖК "Северный"</p>
                </div>
                <button className="w-full bg-gray-100 text-gray-700 font-bold py-2.5 rounded-lg text-sm border">
                  Принять заказ
                </button>
              </div>
            </div>
          </div>
        </PhoneScreen>

        {/* Экран 5: Tracking URL / Деталка (Управление) */}
        <PhoneScreen title="Трекинг #CF-1025" showBack={true}>
          <div className="flex flex-col h-full">

            {/* Имитация карты */}
            <div className="h-48 bg-blue-50 relative overflow-hidden border-b flex items-center justify-center">
              {/* Декоративная сетка карты */}
              <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'radial-gradient(#4b5563 1px, transparent 1px)', backgroundSize: '16px 16px' }}></div>
              <div className="relative z-10 flex flex-col items-center">
                <div className="w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center mb-1 border-2 border-blue-500 animate-pulse">
                  <Navigation size={24} className="text-blue-500" />
                </div>
                <div className="bg-white px-2 py-1 rounded shadow text-[10px] font-bold text-gray-700">
                  [Карта: Местоположение]
                </div>
              </div>
              <div className="absolute bottom-2 right-2 bg-white p-1.5 rounded shadow text-xs flex gap-1 items-center">
                 <Clock size={12} className="text-gray-500"/> Обновлено: 14:02
              </div>
            </div>

            <div className="p-4 flex-1 flex flex-col">
              <div className="bg-white rounded-xl p-4 border shadow-sm mb-4">
                <h3 className="text-sm font-bold text-gray-800 mb-4">Статус доставки</h3>

                <div className="relative">
                  <div className="absolute left-[9px] top-2 bottom-2 w-0.5 bg-gray-200 z-0"></div>

                  <div className="relative z-10 flex gap-3 mb-4">
                    <div className="w-5 h-5 rounded-full bg-blue-500 flex items-center justify-center shrink-0">
                      <CheckCircle size={12} className="text-white" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-gray-800">Заказ создан</p>
                      <p className="text-xs text-gray-400">13:45</p>
                    </div>
                  </div>

                  <div className="relative z-10 flex gap-3 mb-4">
                    <div className="w-5 h-5 rounded-full bg-blue-500 flex items-center justify-center shrink-0 shadow-[0_0_0_3px_white]">
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                    <div>
                      <p className="text-sm font-bold text-blue-600">В пути (IN_TRANSIT)</p>
                      <p className="text-xs text-gray-500 mt-1">Курьер забрал посылку и направляется к вам.</p>
                    </div>
                  </div>

                  <div className="relative z-10 flex gap-3">
                    <div className="w-5 h-5 rounded-full bg-gray-200 border-2 border-white shrink-0"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-400">Доставлен</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Секция действий для Курьера (или инфо о курьере для клиента) */}
              <div className="bg-gray-800 rounded-xl p-4 mt-auto">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center">
                    <User size={20} className="text-white" />
                  </div>
                  <div className="flex-1">
                    <p className="text-xs text-gray-400">Назначенный курьер</p>
                    <p className="text-sm font-semibold text-white">Алексей С.</p>
                  </div>
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center cursor-pointer">
                    <Phone size={14} className="text-white" />
                  </div>
                </div>

                {/* Имитация UI обновления статуса (для Курьера) */}
                <div className="border-t border-gray-700 pt-3 mt-1">
                  <p className="text-[10px] text-gray-400 mb-2 uppercase tracking-wider">Управление (Только для курьера)</p>
                  <select className="w-full bg-gray-700 text-white text-sm border-none rounded-lg p-2.5 mb-2 outline-none" disabled>
                    <option>IN_TRANSIT (В пути)</option>
                    <option>DELIVERED (Доставлен)</option>
                  </select>
                  <button className="w-full bg-blue-600 text-white font-semibold py-2.5 rounded-lg text-sm hover:bg-blue-500 transition-colors">
                    Обновить статус
                  </button>
                </div>
              </div>
            </div>
          </div>
        </PhoneScreen>

      </div>
    </div>
  );
}