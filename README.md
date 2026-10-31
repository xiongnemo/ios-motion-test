# Motion Test

一个看 iOS 运动传感器的小应用：加速度计、陀螺仪、姿态（roll / pitch / yaw）、重力、用户加速度、磁航向的实时数值，
上面还有一个 3D 手机模型，跟着手机的姿态转。点一下模型，它就以当前姿态为起点，重新正对着你。

最早是为了在 Redmi K40（alioth）上跑的 iOS 16.5 移植里测传感器而写的，普通 iOS 设备上一样能用。

- 包名：`com.anzupop.com.ios.motiontest`
- 最低 iOS 15.0，只用 UIKit、Core Motion、Core Animation（3D 模型用 `CATransformLayer`，不需要 Metal）
- 图标由 `mkicon.py` 生成（纯 Python，没有 asset catalog）

## 编译

产物是 `build/MotionTest.ipa`，没有苹果签名，只适合不校验签名的系统，比如上面那个移植，或者越狱设备。

```sh
./build.sh                                                   # macOS，用 Xcode
CC=xnu-clang SDK=$THEOS/sdks/iPhoneOS16.5.sdk ./build.sh     # Linux / WSL，需要能链接 iOS 的 clang + ld64
```

也可以在 GitHub Actions 里手动运行 `build`（或推一个 `v*` 标签），IPA 会作为运行的产物保存。

## 文件

| 文件 | 作用 |
|---|---|
| `main.m` | 整个应用（界面、Core Motion、3D 模型） |
| `Info.plist` | 包名、版本、图标 |
| `mkicon.py` | 生成 60×60 @2x / @3x 图标 |
| `build.sh` | 编译并打包成 IPA |
