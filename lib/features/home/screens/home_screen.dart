import 'dart:async';

import 'package:flutter/material.dart';
import 'package:meetwalks/features/home/utils/team_settings_util.dart';
import 'package:meetwalks/theme.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  dynamic _currentTime = '';

  @override
  void initState() {
    super.initState();
    _updateTime();
    Timer.periodic(Duration(seconds: 1), (Timer t) => _updateTime());
  }

  void _updateTime() {
    final now = DateTime.now();
    setState(() {
      _currentTime =
          '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/backgrounds/bg_night.jpg"),
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(
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
                ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    shape: CircleBorder(),
                    disabledForegroundColor: Colors.amber,
                    fixedSize: Size(150, 150),
                    backgroundColor: Colors.lightBlue.withValues(alpha: 0.6),
                    foregroundColor: Colors.lightBlue,
                  ),
                  child: Icon(Icons.search, size: 100, color: Colors.white),
                ),
                SizedBox(height: 23),
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      setVisibalitiBNB();
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
              child:
                  isBottomNavigationBarVisibaliti
                      ? Container(
                        decoration: BoxDecoration(
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
                                  .center, // Распределение элементов
                          children: [
                            IconButton(
                              onPressed: () {},
                              icon: Icon(
                                Icons.home,
                                size: 60,
                                color: Colors.white,
                              ),
                            ),
                            SizedBox(width: 70),
                            IconButton(
                              onPressed: () {
                                Navigator.pushNamed(context, "/company");
                              },
                              icon: Icon(
                                Icons.group,
                                size: 60,
                                color: Colors.white,
                              ),
                            ),
                            SizedBox(width: 70),
                            IconButton(
                              onPressed: () {},
                              icon: Icon(
                                Icons.person,
                                size: 60,
                                color: Colors.white,
                              ),
                            ),
                          ],
                        ),
                      )
                      : Dismissible(
                        key: Key("Настройки"),
                        direction: DismissDirection.down,
                        onDismissed: (DismissDirection direction) {
                          setState(() {
                            isBottomNavigationBarVisibaliti =
                                !isBottomNavigationBarVisibaliti;
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
                      ),
            ),
          ],
        ),
      ),
    );
  }
}
