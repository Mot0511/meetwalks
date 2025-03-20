import 'dart:async';

import 'package:flutter/material.dart';

class CompanyScreen extends StatefulWidget {
  const CompanyScreen({super.key});

  @override
  State<CompanyScreen> createState() => _CompanyScreenState();
}

class _CompanyScreenState extends State<CompanyScreen> {
  dynamic _currentTime = "";

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
        child: Expanded(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
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
                  height: 80,
                  padding: EdgeInsets.symmetric(
                    vertical: 10.0,
                    horizontal: 20.0,
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Название компании",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 25,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            "12 июня",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 15,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          Text(
                            _currentTime,
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 15,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                child: Padding(
                  padding: EdgeInsets.symmetric(horizontal: 10),
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.lightBlue.withValues(alpha: 0.6),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        Expanded(
                          child: Container(), // здесь сообщения
                        ),
                        Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Row(
                            children: [
                              Expanded(
                                child: TextField(
                                  style: TextStyle(color: Colors.white),
                                  decoration: InputDecoration(
                                    hintText: "Введи что-нибудь",
                                    hintStyle: TextStyle(color: Colors.white),
                                    fillColor: Colors.white, // Цвет заливки
                                    focusColor: Colors.white,
                                    border: OutlineInputBorder(
                                      borderSide: BorderSide(
                                        width: 2.0, // Толщина рамки
                                        color: Colors.white, // Цвет рамки
                                      ),
                                    ),
                                    enabledBorder: OutlineInputBorder(
                                      borderSide: BorderSide(
                                        width: 2.0,
                                        color: Colors.white,
                                      ),
                                    ),
                                    focusedBorder: OutlineInputBorder(
                                      borderSide: BorderSide(
                                        width: 2.0,
                                        color: Colors.white,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(width: 7),
                              Container(
                                height: 45,
                                width: 45,
                                decoration: BoxDecoration(
                                  color: Colors.green,
                                  border: Border.all(color: Colors.green),
                                  borderRadius: BorderRadius.circular(5),
                                ),
                                child: IconButton(
                                  onPressed: () {},
                                  icon: Icon(Icons.add, color: Colors.white),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              SizedBox(height: 10),
              Container(
                decoration: BoxDecoration(
                  color: Colors.lightBlue.withValues(alpha: 0.6),
                ),
                height: 80,
                padding: EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      onPressed: () {
                        Navigator.pushNamed(context, "/home");
                      },
                      icon: Icon(Icons.home, size: 60, color: Colors.white),
                    ),
                    SizedBox(width: 70),
                    IconButton(
                      onPressed: () {},
                      icon: Icon(Icons.group, size: 60, color: Colors.white),
                    ),
                    SizedBox(width: 70),
                    IconButton(
                      onPressed: () {},
                      icon: Icon(Icons.person, size: 60, color: Colors.white),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
