import 'package:flutter/material.dart';

ThemeData theme = ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
  textTheme: TextTheme(
    titleMedium: TextStyle(
      color: Colors.white,
      fontSize: 20,
      fontWeight: FontWeight.w500,
    ),
  ),
  scaffoldBackgroundColor: Colors.transparent
);

TextStyle mediumTextStyle = TextStyle(color: Colors.white, fontSize: 20);
