# Device configuration for Snapdragon 750G (SM7225) SOC Devices

Branch `lineage-24.0` is the common tree of the unofficial **LineageOS 24.0 (Android 17)** port for
the Samsung Galaxy Tab S7 FE LTE (**SM-T735**, `gts7xllite`). It is tested on that device only.
See [android_device_samsung_gts7xllite](https://github.com/lelelol/android_device_samsung_gts7xllite/tree/lineage-24.0)
for the full list of repositories, status and credits.

Notable lineage-24.0 changes (one commit each):
- hardware video through an OMX stack built from source (Android 17 has no OMX service and the
  Android 11 OMX blobs are ABI-incompatible with it);
- Samsung VINTF declarations (camera.provider 2.6, snap, HDCP, media converter), stock camera
  device impls, gatekeeper SELinux, media.converter relinked against common-V2-ndk;
- battery: no face HAL / cass restart loops, stock swap readahead, powerhint L3 nodes and GPU floor;
- the lineage-22.2 LCD overlay tweaks (no AOD, no doze dream, GPU color transform).

> **Vibe-coded**: written with heavy help from an AI coding assistant (Claude Code). Reviews welcome.

## SoC specifications
Basic        | Spec Sheet
------------:|:----------------------
Litograhy    | 8nm
CPU          | Octa-core (6x1.8ghz Kryo 570 & 2x2.2ghz Cortex A77)
GPU          | Adreno 619
Architecture | 64bits, ARMv8-A (A32, A64)
L3 cache     | 3 MB
Features     | X52 LTE Modem, Hexagon 694 DSP, Specra 355L ISP

![SOC](https://files.tecnoblog.net/wp-content/uploads/2020/09/snapdragon-750g-slide.jpg)

## Credits
Blitzhagen (original trees), the samsung-sm7225 team (lineage-23.2 base: Aflaungos, bgcngm, mikeNG,
Simon1511, luk1337 and others), The LineageOS Project, Qualcomm/qcom-caf, Samsung, the Xiaomi
SM8250-common LineageOS vendor tree (Widevine), Google/AOSP. Built with the help of Claude Code.

## Copyright

```
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
```
