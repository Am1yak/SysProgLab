### Pinout таблиця

| Пін МК | Номер AF | Периферійний блок і сигнал | Роз'єм Nucleo | Пін пристрою | Рівень напруги | Наявність Pull-up / Pull-down | Обґрунтування / Джерело |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PA0 | GPIO (None) | ADC1_IN0 | CN7-28 | LDR1 Output (Top/North) | 0–3.3V | Pull-down (10k Ом на модулі) | Виділений аналоговий канал ADC1; відсутні конфлікти з набором периферії [DS10471, Tab. 9].
| PA1 | GPIO (None) | ADC1_IN1 | CN7-30 | LDR2 Output (Bottom/South) | 0–3.3V | Pull-down (10k Ом на модулі) | Суміжний аналоговий вхід для швидкої регулярної групи ADC1 [DS10471, Tab. 9].
| PA2 | AF7 | USART2_TX | CN10-35 | ST-LINK Virtual COM (TX) | 3.3V TTL | Ні (вбудовано в ST-LINK) | Фіксована апаратна траса на платі Nucleo-64 для відлагодження через USB [UM1724, Sec. 6.8].
| PA3 | AF7 | USART2_RX | CN10-37 | ST-LINK Virtual COM (RX) | 3.3V TTL | Ні (вбудовано в ST-LINK) | Фіксована апаратна траса на платі Nucleo-64 для відлагодження через USB [UM1724, Sec. 6.8].
| PA4 | GPIO (None) | ADC1_IN4 | CN7-32 | LDR3 Output (Left/East) | 0–3.3V | Pull-down (10k Ом на модулі) | Аналоговий вхід ADC1; не перетинається з SPI1_NSS [DS10471, Tab. 9].
| PA5 | GPIO (None) | GPIO_Output | CN10-11 | Green LED (LD2) | 3.3V | Pull-down (на платі Nucleo) | Вбудований індикаторний світлодіод плати Nucleo [UM1724, Sec. 6.5].
| PA6 | AF2 | TIM3_CH1 | CN10-13 | Servo Azimuth Signal (PWM) | 3.3V TTL | Ні (Керування CMOS) | Канал таймера TIM3 з підтримкою PWM generation для сервоприводу [DS10471, Tab. 9].
| PA7 | AF2 | TIM3_CH2 | CN10-15 | Servo Elevation Signal (PWM) | 3.3V TTL | Ні (Керування CMOS) | Другий канал TIM3 для незалежного керування віссю елевації [DS10471, Tab. 9].
| PB0 | GPIO (None) | ADC1_IN8 | CN7-34 | LDR4 Output (Right/West) | 0–3.3V | Pull-down (10k Ом на модулі) | Канал ADC1; обрано для збалансованого трасування плати [DS10471, Tab. 9].
| PB10 | AF5 | SPI2_SCK | CN10-25 | W25Q64 Flash CLK | 3.3V | Ні (Push-Pull AF) | Тактова лінія SPI2 [DS10471, Tab. 9].
| PC2 | AF5 | SPI2_MISO | CN7-35 | W25Q64 Flash DO (IO1) | 3.3V | Pull-up (Внутрішній МК, 40k Ом) | Лінія шини SPI2 Master In Slave Out [DS10471, Tab. 9].
| PC3 | AF5 | SPI2_MOSI | CN7-37 | W25Q64 Flash DI (IO0) | 3.3V | Ні (Push-Pull AF) | Лінія шини SPI2 Master Out Slave In [DS10471, Tab. 9].
| PB12 | GPIO (None) | GPIO_Output | CN10-16 | W25Q64 Flash CS (#CE) | 3.3V | Pull-up (Внутрішній МК, 40k Ом) | Програмне керування Chip Select (FLASH_CS) для запобігання хибним спрацьовуванням [DS10471, Tab. 9].
| PC13 | EXTI13 | GPIO_EXTI13 | CN7-23 | Blue PushButton (B1) | 3.3V | Pull-up (на платі Nucleo) | Вбудована кнопка користувача з перериванням по спаду (Falling Trigger) [UM1724, Sec. 6.4].

### Бюджет живлення

| Пристрій | Джерело живлення | Напруга (V) | Струм у робочому режимі | Піковий струм | Запас по струму / Примітка | 
| --- | --- | --- | --- | --- | --- | 
| STM32F411RET6 MCU | Nucleo 3.3V (LDO) | 3.3V | 20.0 mA | 50.0 mA | Живлення від вбудованого регулятора ST-LINK | 
| W25Q64 SPI Flash | Nucleo 3.3V (LDO) | 3.3V | 4.0 mA | 25.0 mA (Write/Erase) | Живлення від ліній шини 3.3V Nucleo
| 4x LDR Сенсори | Nucleo 3.3V (LDO) | 3.3V | 1.3 mA | 2.0 mA | $I = \frac{3.3 V} {10kO} \times 4 \approx 1.32 mA$
| 2x Сервоприводи (SG90) | Окремий БП 5V | 5.0V | 200.0 mA | 1200.0 mA (Stall) | Критично: Потрібне окреме джерело



### Розрахунок дерев тактування

Джерело тактування: HSI (16 MHz) >> PLL (PLLM=16, PLLN=336, PLLP=4).

Системна частота ядра (SYSCLK / HCLK):
$$f_{\text{SYSCLK}} = \frac{16\text{ MHz}}{16} \times 336 \div 4 = 84\text{ MHz}$$

Шина APB1 Peripheral Clock ($PCLK1$): $DIV2 \rightarrow f_{\text{APB1}} = 42\text{ MHz}$.

Шина APB1 Timer Clock ($TIMCLK1$): $DIV2 \times 2 \rightarrow f_{\text{APB1\_TIM}} = 84\text{ MHz}$.

### Параметри шини SPI2 (Flash-пам'ять W25Q64)
Режим роботи: Master, Full-Duplex, SPI Mode 0 ($CPOL=0, CPHA=0$).  
Розрахунок частоти: При дільнику $Prescaler = 2$ від $f_{\text{APB1}} = 42\text{ MHz}$:  
$$f_{\text{SPI2}} = \frac{42\text{ MHz}}{2} = 21.0\text{ MBits/s}$$

### Розрахунок TIM3 PWM (Керування сервоприводами 50 Гц)
Для стандартних сервоприводів серії SG90 потрібна частота $50\text{ Hz}$ (період $T = 20\text{ ms}$):
$Prescaler\ (PSC) = 83$
$Auto-Reload\ Register\ (ARR) = 19999$

$$f_{\text{PWM}} = \frac{f_{\text{APB1\_TIM}}}{(PSC + 1) \cdot (ARR + 1)} = \frac{84\,000\,000}{(83 + 1) \cdot (19999 + 1)} = \frac{84\,000\,000}{84 \cdot 20000} = 50\text{ Hz}$$

Такт лічильника складає $1\ \mu\text{s}$. Тривалість імпульсу регулюється значеннями регістрів порівняння $CCR1$ та $CCR2$:
$0^\circ$ (Мінімальний кут): $CCR = 1000$ ($1.0\text{ ms}$).  
$90^\circ$ (Нейтральне положення): $CCR = 1500$ ($1.5\text{ ms}$).  
$180^\circ$ (Максимальний кут): $CCR = 2000$ ($2.0\text{ ms}$).  