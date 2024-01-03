<template>
    
    <header>
        <div class="div-logo">
            <img class="logo" src="@/assets/images/landing/logo.svg" draggable="false"/>
            <img class="logo2" src="@/assets/images/landing/logo2.svg" draggable="false"/>
        </div>
        <div class="group">
            <a  class="text-wrapper" href="#about">О нас</a>
            <a  class="text-wrapper" href="#inform">Наши особенности</a>
            <div class="overlap-group">
                <button class="tx text-wrapper-1" >
                    <a href="#rec" class="text-rec">Авторизация</a>
                </button>
                <div class="div-aicon">
                    <a class="subtract-1" href="#"></a>
                    <a class="subtract-2" href="#"></a>
                    
                </div>
            </div>
        </div>    
    </header> 
    <section-1>
        <div class="contener-about">
            <div class="text">
                <h1>Bubble</h1>
                <h3>blow out with friends</h3>
                <div class="b1">
                    <button class="text-wrapper-1" >
                        <a href="#rec" class="text-rec">Авторизация</a>
                    </button>
                </div>
            </div>
            <img class="rut-p" src="@/assets/images/landing/p-rute.svg" draggable="false"/>
        </div>
    </section-1>
    <section-2>
        <div class="overlap-group-2">
            <div class="bubbles">
                <img class="image1" src="@/assets/images/landing/bubbles.svg" draggable="false"/>
                <img class="image2" src="@/assets/images/landing/img2.svg" draggable="false"/>
            </div>
            <div class="text-about" id="about">
                <h2 class="">About us</h2>
                <p class="div">Наш web-сервис “Bubble” представляет собой современную платформу для организации аудио-видеоконференций с обменом сообщениями и возможностью создавать доски задач. Мы разработали эту программу с учетом потребностей различных пользователей, включая школьников, студентов, преподавателей и офисных работников. Web-сервис разработан с использованием современных технологий, обеспечивая его безопасность и простоту использования. </p>
            </div>
        </div>
    </section-2>
    <section-3>
       <div class="inform-about-us" id="inform">
            <h2 class="text-inform">Our features</h2>
            <div class="cards">
                <div class="card">
                    <p class="text-card">Аудио и видео-связь</p>
                    <div class="text-and-img">
                        <img class="img-card" src="@/assets/images/landing/Rectangle1.svg" draggable="false"/>
                        <h6 class="text-card-info">Возможность проведения аудио- и видеоконференций между двумя и более пользователями. Управление функциями аудио- и видеосвязи</h6>
                    </div>
                </div>
                <div class="card">
                    <p class="text-card">Планирование</p>
                    <div class="text-and-img">
                        <img class="img-card" src="@/assets/images/landing/Rectangle2.svg" draggable="false"/>
                        <h6 class="text-card-info">Создание и управление досками задач, включая возможность создавать карточки с задачами, устанавливать сроки выполнения, отслеживать статус и добавлять описание и файлы.</h6>
                    </div>
                </div>
                <div class="card">
                    <p class="text-card">Текстовые чаты</p>
                    <div class="text-and-img">
                        <img class="img-card" src="@/assets/images/landing/Rectangle3.svg" draggable="false"/>
                        <h6 class="text-card-info">Создание групп для общения по определенным темам или проектам, с возможностью отправки сообщений, аудио и видеосвязи, а также обмена файлами.</h6>
                    </div>
                </div>
                <div class="card">
                    <p class="text-card">Создание команд</p>
                    <div class="text-and-img">
                        <img class="img-card" src="@/assets/images/landing/Rectangle4.svg" draggable="false"/>
                        <h6 class="text-card-info">Возможность инициировать конференцию, приглашать других пользователей и общаться в режиме реального времени.</h6>
                    </div>
                </div>
            </div>       
       </div>
    </section-3>
    <section-4>
        <div class="contener-r" id="rec">
            <div class="view" >
                <div class="r-group" >
                    <form class="rectangle">
                        <h4 class="text-r-a">Регистрация/Авторизация</h4>
                        <h5 class="text-login">Логин</h5>
                        <input type="text" name="logo">
                        <h5 class="text-par">Пароль</h5>
                        <input type="text" name="password">
                        <button class="text-wrapper-2 login-button" href="#">Войти</button>
                    </form>
                </div>
            </div>
            
        </div>
    </section-4>
    <footer>
        
        <a onclick="look('link1'); return false;" class="footer-tv"  ></a>
        <img id="link1" class="man" src="@/assets/images/landing/men.svg"  style="display: none;" >
    </footer>
    <div id="snow-container"></div>
</template>

<script>

function startSnow() {
            const snowContainer = document.getElementById("snow-container"); // получение элемента с идентификатором "snow-container" из документа
            const snowContent = ['&#10052', '&#10053', '&#10054'] // массив снежинок

            const random = (num) => { // ф-ция принимает число в качестве аргумента и возвращает случайное целое число от 0 до числа - 1
              return Math.floor(Math.random() * num);
            }

            const RandomStyles = () => { //ф-ция генерирует случайные стили (топ, лево, длительность анимации и размер) для снежинки
              const top = random(100);
              const left = random(100);
              const dur = random(10) + 10;
              const size = random(25) + 25;
              return `
                top: -${top}%;
                left: ${left}%;
                font-size: ${size}px;
                animation-duration: ${dur}s;
              `;
              /*
              Значение стиля "top" - отрицательный процент (снежинка начинает падение за пределами экрана).
              Значение стиля "left" - случайный процент, (снежинка появляется в случайном месте на горизонтальной оси).
              Длительность анимации и размер снежинки - случайные значения.
              */
            }

            const createSnow = (num) => { // принимает число в качестве аргумента и создает указанное количество снежинок
              for (var i = num; i > 0; i--) { // создания указанного количества снежинок
                var snow = document.createElement("div"); //элемент div получает класс "snow"
                snow.className = "snow";
                snow.style.cssText = RandomStyles(); //Применяются случайные стили из функции getRandomStyles
                snow.innerHTML = snowContent[random(3)] // выбирается случайный вид снежинки
                snowContainer.append(snow); //Созданный элемент добавляется внутрь элемента snowContainer
              }
            }

            window.addEventListener("load", () => { // создаётся 30 снежинок
              createSnow(30)
            });
        }

export default {
    name: 'LandingMain',
    components: {
    },
    methods: {
    },
    setup() {
        return {}
    },
    mounted() {
        startSnow();
    }
}
</script>

<style></style>