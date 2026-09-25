# Hardware Component Specification for the "Heliostat" Project

This document details the technical specifications, interfaces, pinouts, register maps, and power requirements for all hardware components used in the solar tracker lab project.

---

## 1. Microcontroller: NUCLEO-F411RE (STM32F411RET6)
* **Manufacturer / Datasheet:** STMicroelectronics — [STM32F411xD/xE Datasheet (DS10472)](https://www.st.com/resource/en/datasheet/stm32f411re.pdf)
* **Core & Frequency:** ARM Cortex-M4 with FPU, operating frequency up to 100 MHz (Project configuration: 84 MHz via PLL, DS10472 p. 15).
* **Memory:** 512 KB Flash, 128 KB SRAM (DS10472 p. 14).
* **Peripherals Used:**
  * **ADC1:** 12-bit ADC, DMA (PA0, PA1, PA4, PB0).
  * **TIM3:** PWM generation for servos (PA6, PA7).
  * **SPI2:** Full-duplex Master, SPI Mode 0, up to 21 Mbit/s.
  * **USART2:** Asynchronous UART (PA2/TX, PA3/RX) at 115200 baud.
* **Power:** 3.3V internal LDO regulator. Maximum 3V3 rail current capability is approximately 300 mA.

---

## 2. Flash Memory: Winbond W25Q64JV (SPI Flash)
* **Manufacturer / Datasheet:** Winbond Electronics — [W25Q64JV Datasheet Rev G](https://www.alldatasheet.com/datasheet-pdf/pdf/1243794/WINBOND/W25Q64JV.html)
* **Interface & Bus:**
  * **Bus:** SPI (Mode 0: CPOL=0, CPHA=0 and Mode 3: CPOL=1, CPHA=1), p. 14.
  * **Max Frequency:** Up to 133 MHz (p. 94). In our project: 21 MHz (APB1 / 2).
* **Pin Mapping:**
  * `VCC`: 2.7V – 3.6V (connected to Nucleo **3V3**).
  * `GND`: Common ground.
  * `CLK (SCK)`: `PB10` (SPI2_SCK).
  * `DI (IO0/MOSI)`: `PC3` (SPI2_MOSI).
  * `DO (IO1/MISO)`: `PC2` (SPI2_MISO).
  * `/CS` (Chip Select): `PB12` (Software GPIO Output, active low).
  * `/WP` (Write Protect) & `/HOLD`: Pulled high to VCC (3.3V).
* **Register Map & Identification:**
  * **JEDEC ID Command (`0x9F`):** Returns 3 identification bytes: Manufacturer ID = `0xEF`, Memory Type = `0x40`, Capacity = `0x17` (64 Mbit / 8 MB), pp. 23, 67.
  * **Status Register 1 Read (`0x05`):** `BUSY` bit (Bit 0) indicates an ongoing write/erase operation, p. 22.
  * **Write Enable (`0x06`):** Must be sent before every write or erase operation, p. 27.
* **Power Consumption:**
  * **Read Current:** 4–10 mA (p. 92).
  * **Write/Erase Current:** Up to 25 mA (p. 92).
  * **Source:** Can be safely powered from the Nucleo **3V3 Pin**.

---

## 3. Photoresistors: GM5528 (4x LDR Quadrant Array)
* **Manufacturer / Datasheet:** Topila / LDR Datasheet Spec Sheet — [GM5528 Photoresistor Datasheet](https://www.sparkinter.com/pdf/120300-0056590.pdf)
* **Type & Interface:**
  * **Interface:** Analog voltage divider $\rightarrow$ **ADC1** (12-bit).
  * **Voltage Range:** $0 - 3.3\text{ V}$ (linear ADC response from $0$ to $4095$).
* **Circuit Topology:**
  * Upper leg of divider: GM5528 LDR (connected to **3V3**).
  * Lower leg of divider: Fixed $10\text{ k}\Omega$ resistor (connected to **GND**).
  * Midpoint (Output Voltage): Connected to ADC channels (`PA0` - LDR1, `PA1` - LDR2, `PA4` - LDR3, `PB0` - LDR4).
* **Characteristics:**
  * Resistance at 10 lux (Light): $8 - 20\text{ k}\Omega$.
  * Dark Resistance (0 lux): $> 1\text{ M}\Omega$.
* **Power & Current:**
  * At peak illumination, divider resistance $\approx 8\text{ k}\Omega + 10\text{ k}\Omega = 18\text{ k}\Omega$.
  * Maximum current per divider: $I = \frac{3.3\text{ V}}{18\text{ k}\Omega} \approx 0.18\text{ mA}$.
  * Total current for all 4 photoresistors: $< 1\text{ mA}$.
  * **Source:** Safely powered from the Nucleo **3V3 Pin**.

---

## 4. Servos: TowerPro / Micro Servo SG92R (2x)
* **Manufacturer / Datasheet:** TowerPro — [SG92R Digital Micro Servo Spec](https://www.towerpro.com.tw/product/sg92r-7/)
* **Control Interface:**
  * **Type:** PWM (Pulse Width Modulation), $50\text{ Hz}$ ($20\text{ ms}$ period).
  * **Pulse Width:** $1.0\text{ ms}$ ($0^\circ$ angle) – $1.5\text{ ms}$ ($90^\circ$ angle) – $2.0\text{ ms}$ ($180^\circ$ angle).
  * **Channels:** `PA6` (TIM3_CH1 - Azimuth), `PA7` (TIM3_CH2 - Elevation).
* **Pinout:**
  * Brown / Black: `GND`
  * Red: `VCC` ($4.8\text{ V} - 6.0\text{ V}$)
  * Orange / Yellow: `Signal PWM` (3.3V Logic Compliant)
* **Power & Current Warnings (CRITICAL!):**
  * **Operating Current:** $100 - 220\text{ mA}$ per servo during motion.
  * **Stall Current:** Up to $650 - 700\text{ mA}$ per servo!
  * **Power Source:** Servos must be powered from the **5V Pin (USB Power)** or an external $5\text{ V}$ power supply sharing a common ground (`GND`) to prevent MCU brownout resets.

---

## 5. USB-UART Adapter: FT232RL / Onboard ST-Link VCP
* **Manufacturer / Datasheet:** FTDI Chip — [FT232RL Datasheet](https://ftdichip.com/wp-content/uploads/2020/08/DS_FT232R.pdf)
* **Interface:**
  * **UART:** 115200 baud, 8 data bits, no parity, 1 stop bit (8N1).
  * **Pins:** `PA2` (MCU TX $\rightarrow$ Adapter RX), `PA3` (MCU RX $\leftarrow$ Adapter TX).
* **Power:** Powered via the PC's USB bus ($5\text{ V}$), logic levels on MCU side are $3.3\text{ V}$.