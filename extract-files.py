#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)


namespace_imports = [
    'device/samsung/sm7225-common',
    'hardware/qcom-caf/sm8250',
    'hardware/qcom-caf/wlan',
    'hardware/samsung',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    # SM-T735 Android 11-era blobs: drop build-time deps that have no module on 16;
    # they resolve at runtime from the VNDK v30 apex or the vendor partition.
    (
        'android.hardware.common-V1-ndk_platform',
        'android.hardware.light-V1-ndk_platform',
        'libsdm-color',
        'libstagefright_bufferqueue_helper_vendor',
        'sound_trigger.primary.lito',
        'vendor.samsung.frameworks.security.dsms-V1-ndk_platform',
        'vendor.samsung.hardware.hyper-V2-ndk_platform',
        'vendor.samsung.hardware.media.converter-V1-ndk_platform',
        'vendor.samsung.hardware.security.fkeymaster-V1-ndk_platform',
        'vendor.samsung.hardware.security.widevine.keyprov-V1-ndk_platform',
        'vendor.samsung.hardware.snap-V1-ndk_platform',
        'vintf-codecsolution-V2-ndk_platform',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/libsec-ril.so': blob_fixup()
        .binary_regex_replace(b'ril.dds.call.ongoing', b'vendor.calls.slot_id')
        .sig_replace(
            '60 0e 40 f9 82 0c 80 52 24 00 80 52 e1 03 15 aa 08 00 40 f9 e3 03 14 aa',
            '60 0e 40 f9 82 0c 80 52 24 00 80 52 e1 03 15 aa 08 00 40 f9 03 00 80 d2'
        ),
    ('vendor/lib64/hw/gatekeeper.mdfpp.so', 'vendor/lib64/libkeymaster_helper.so', 'vendor/lib64/libskeymaster4device.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
    # SM-T735 blobs (option B): shims validated on lineage-22.2
    ('vendor/lib/unihal_main@2.15.so', 'vendor/lib64/unihal_main@2.15.so',
     'vendor/lib/libscaler_hw.unifunc.so', 'vendor/lib64/libscaler_hw.unifunc.so',
     'vendor/lib/libscaler_sw.unifunc.so', 'vendor/lib64/libscaler_sw.unifunc.so'): blob_fixup()
        .add_needed('libui_compat_shim.so'),
    'vendor/lib/hw/audio.primary.lito.so': blob_fixup()
        .patch_file('patches/audio_primary_lito_fixup.py'),
    # Android 11 codec seccomp policies only allow mremap(MAYMOVE|FIXED); current bionic/scudo
    # also calls mremap(MAYMOVE), so the codec services died with SIGSYS at start-up.
    ('vendor/etc/seccomp_policy/samsung.software.media.c2-base-policy',
     'vendor/etc/seccomp_policy/codec2.vendor.base-arm.policy'): blob_fixup()
        .regex_replace(r'(?m)^mremap: arg3 == 3$', 'mremap: arg3 == 3 || arg3 == MREMAP_MAYMOVE'),
    # Android 11 camera blobs import common::V1_0::helper symbols that current AOSP renamed to
    # common::helper (same ABI); camera_shim/ re-exports the old names.
    ('vendor/lib64/vendor.samsung.hardware.camera.provider@4.0-legacy.so',
     'vendor/lib64/vendor.samsung.hardware.camera.device@5.0-impl.so'): blob_fixup()
        .add_needed('libcamera_helper_v1_0_shim.so'),
    'vendor/lib64/libSecC2ComponentStore.so': blob_fixup()
        .add_needed('libc2compat_shim.so'),
    ('vendor/lib/hw/android.hardware.audio@6.0-impl.so', 'vendor/lib64/hw/android.hardware.audio@6.0-impl.so',
     'vendor/lib/libaudiofoundation.so', 'vendor/lib64/libaudiofoundation.so',
     'vendor/lib/libeffectsconfig.so', 'vendor/lib64/libeffectsconfig.so'): blob_fixup()
        .add_needed('libaudiotypeconv_shim.so'),
    ('vendor/lib64/nfc_nci_nxpsn.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/lib64/libdpps.so'): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    # SM-T735 blob: RegisterIPostProcService() reconfigures the provider's already started HIDL
    # threadpool and current libhidlbase aborts; NOP the configureRpcThreadpool(4, true) call.
    'vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .sig_replace('9A 0A 00 94', '1F 20 03 D5')
        .sig_replace('80 00 80 52 21 00 80 52 CE 09 00 94', '80 00 80 52 21 00 80 52 1F 20 03 D5'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm7225-common',
    'samsung',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()