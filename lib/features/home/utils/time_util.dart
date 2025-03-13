String nowTime = "";
void getTimeNow() {
  DateTime time = DateTime.now();
  // Форматируем время в "чч:мм"
  nowTime = '${time.hour.toString().padLeft(2, '0')}:${time.minute.toString().padLeft(2, '0')}';
}
