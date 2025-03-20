import 'package:flutter/material.dart';

class Navbar extends StatelessWidget {
  const Navbar({super.key, required this.onTap});
  final onTap;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.lightBlue.withValues(alpha: 0.6),
      ),
      height: 80, // Высота панели 1/15 экрана
      padding: EdgeInsets.symmetric(
        horizontal: 20.0,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround, 
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          IconButton(
            onPressed: () => onTap(0),
            icon: Icon(
              Icons.home,
              size: 60,
              color: Colors.white,
            ),
          ),
          SizedBox(width: 70),
          IconButton(
            onPressed: () => onTap(1),
            icon: Icon(
              Icons.group,
              size: 60,
              color: Colors.white,
            ),
          ),
          SizedBox(width: 70),
          IconButton(
            onPressed: () => onTap(2),
            icon: Icon(
              Icons.person,
              size: 60,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}