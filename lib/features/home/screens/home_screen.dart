import 'dart:async';
import 'package:flutter/material.dart';
import 'package:meetwalks/features/home/home.dart';
import 'package:meetwalks/theme.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  dynamic _currentTime = '';
  bool isSettingVisbile = false;
  Timer? timer;

  @override
  void initState() {
    super.initState();
    _updateTime();
    timer = Timer.periodic(Duration(seconds: 1), (Timer t) => _updateTime());
  }

  void _updateTime() {
    final now = DateTime.now();
    setState(() {
      _currentTime =
          '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}';
    });
  }

  void dispose() {
    super.dispose();
    timer?.cancel();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Column(
          children: [
            Padding(
              padding: EdgeInsets.all(10),
              child: Container(
                decoration: BoxDecoration(
                  border: Border.all(
                    color: Colors.lightBlue.withValues(alpha: 0.1),
                  ),
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.lightBlue.withValues(alpha: 0.6),
                ),
                height: 80, // Высота панели 1/15 экрана
                padding: EdgeInsets.symmetric(
                  vertical: 10.0,
                  horizontal: 20.0,
                ),
                child: Row(
                  mainAxisAlignment:
                      MainAxisAlignment
                          .spaceBetween, // Распределение элементов
                  children: [
                    Text(
                      _currentTime,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    Text(
                      'Meetwalks!',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                    Text(
                      '25.C',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: MediaQuery.of(context).size.height / 7),
            SearchWidget(),
            SizedBox(height: 23),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  isSettingVisbile = !isSettingVisbile;
                });
              },
              style: ElevatedButton.styleFrom(
                fixedSize: Size(130, 40),
                backgroundColor: Colors.lightBlue.withValues(alpha: 0.6),
                foregroundColor: Colors.lightBlue.withValues(alpha: 0.6),
                iconSize: 40,
              ),
              child: Icon(Icons.settings, color: Colors.white, size: 20),
            ),
          ],
        ),
        Align(
          alignment: Alignment.bottomCenter,
          child: isSettingVisbile
            ? Dismissible(
                key: Key("Настройки"),
                direction: DismissDirection.down,
                onDismissed: (DismissDirection direction) {
                  setState(() {
                    isSettingVisbile =
                        !isSettingVisbile;
                  });
                },
                child: Container(
                  height: 450,
                  color: Colors.lightBlue.withValues(alpha: 0.6),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      SizedBox(height: 10),
                      Center(
                        child: Text(
                          "Оставляю это тебе",
                          style: mediumTextStyle,
                        ),
                      ),
                    ],
                  ),
                ),
              )
            : SizedBox.shrink()
        ),
      ],
    );
  }
}
