<h1 align="center">Campaign Architect</h1>

<p>Это понятный инструмент для организации, управления и развития кампаний в настольных ролевых играх формата Dungeons & Dragons (и других НРИ). Этот инструмент поможет вам систематизировать весь контент вашей кампании, сохраняя порядок даже в самом масштабном приключении.</p>

<h2>Особенности инструмента:</h2>

<div style="display: flex; justify-content: space-between; gap: 2rem; flex-wrap: wrap;">
    <div style="flex-basis: calc(50% - 1rem);">
        <ul>
            <li><strong>Иерархия элементов кампании:</strong>
            С помощью встроенных папок и вложенности можете группировать персонажей, города, квесты и другие сущности, чтобы легко ориентироваться во всём многообразии своей кампании.</li>
                <pre><code class="language-text">
📂 campaign/
├── 📂 characters/
│   ├── 🧙 gandalf
│   └── 🏹 legolas
├── 📂 locations/
│   ├── 🏰 minas_tirith
│   └── 🌳 lothlorien
└── 📂 plot/
    ├── ⚔️ battle_of_helm's_deep
    └── 💍 destruction_of_the_ring</code></pre>
</ul>
</div>
<div>
<ul>
    <h1 align="center">ТЗ</h1>
    <li>Регистрация и Вход</li>
    <p>Форма регистрации нового пользователя и процедура входа.</p>
    <li>Главное Окно</li>
    <p>Центральное окно содержит рабочую область для управления элементами кампании, фильтры и панели инструментов для быстрой навигации.</p>
    <li>Профиль Пользователя</li>
    <p>Настройка личной информации, управление аккаунтом пользователя.</p>
    <li>Система Файлов и Хранения</li>
    <p>Удобная система хранения элементов кампании.</p>
    <li>Граф Знаний и Временная Шкала</li>
    <p>Инструменты для визуализации взаимосвязей между объектами кампании и временной линии событий.</p>
    <li>Шаблоны</li>
    <p>Предоставляет возможность быстро создавать персонажей, локации, квесты и предметы с использованием готовых шаблонов.</p>
    <li>Поиск и Фильтрация</li>
    <p>Механизмы поиска и фильтрации по заданным параметрам.</p>
</ul>
</div>
<h1 align="center">Пояснительная записка</h1>
<h3>Основная информация</h3>
<p>Campaign Architect</p>
<p>Автор проекта: Шиловский Назар</p>
<p>Campaign Architect - это веб-приложение для мастеров настольных ролевых игр (НРИ), которое позволяет:</p>
<ul>
    <li>Создавать и редактировать кампании.</li>
    <li>Вести заметки по миру, персонажам и сюжетным линиям.</li>
    <li>Управлять игроками (добавлять, удалять, назначать классы персонажей).</li>
    <li>Организовывать сессии с описанием и результатами.</li>
</ul>
<p>Цель проекта: Упростить подготовку к играм, автоматизировать рутинные задачи и создать удобный инструмент для мастеров.</p>
<h3>Реализация</h3>
<p>Создание кампании:<br>
Форма с полями: название, мастер, игровая система.<br>
После создания — автоматический переход в редактор.<br>
Редактор кампании:<br>
Редактируемые поля (текст, выбор статуса, добавление игроков).<br>
Вкладки для заметок, сессий и лора.<br>
Сохранение изменений.<br>
Дизайн:<br>
Стилизованный интерфейс в духе D&D.<br>
Регистрация и вход пользователей<br>
Список всех компаний пользователя с краткой информацией о компании<br>
Возможность загружать изображения (например на заклинания, предметы или монстров)<br>
В этом проекте были использованы: Python, HTML/CSS, JavaScript, Flask ,sqlalchemy</p>
<a href="https://docs.google.com/presentation/d/1m3gnOjGC5OtGxg8OoXU7zPin5DMb9neF/edit?usp=sharing&ouid=111212926852576897666&rtpof=true&sd=true">Ссылка на презентацию</a>
