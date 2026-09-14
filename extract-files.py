#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
	'device/realme/nashc',
	'hardware/oplus',
	'hardware/mediatek',
	'hardware/mediatek/libmtkperf_client'
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('vendor.mediatek.hardware.videotelephony@1.0',): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    'system_ext/lib64/libsink-mtk.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    'system_ext/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),
    'system_ext/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('ims-patches'),
    'odm/lib64/libosenseaidlhalclient.so': blob_fixup()
        .replace_needed('vendor.oplus.hardware.osense.client-V1-ndk_platform.so', 'vendor.oplus.hardware.osense.client-V1-ndk.so'),
    'odm/bin/hw/vendor.oplus.hardware.charger@1.0-service': blob_fixup()
        .add_needed('libbase_shim.so')
	.replace_needed('vendor.oplus.hardware.osense.client-V1-ndk_platform.so', 'vendor.oplus.hardware.osense.client-V1-ndk.so'),
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek', 'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    ('system_ext/etc/init/init.vtservice.rc', 'vendor/etc/init/android.hardware.neuralnetworks@1.3-service-mtk-neuron.rc'): blob_fixup()
        .regex_replace('start', 'enable'),
    'vendor/etc/libnfc-nci.conf': blob_fixup()
        .regex_replace('NFC_DEBUG_ENABLED=0x01', 'NFC_DEBUG_ENABLED=0x00'),
    'vendor/etc/libnfc-nxp.conf': blob_fixup()
        .regex_replace('(NXPLOG_.*_LOGLEVEL)=0x03', '\\1=0x02')
        .regex_replace('NFC_DEBUG_ENABLED=0x01', 'NFC_DEBUG_ENABLED=0x00'),
    'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so': blob_fixup()
        .add_needed('libcamera_metadata_shim.so')
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/libmtkcam_stdutils.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/libmtkcam_featurepolicy.so': blob_fixup()
        .binary_regex_replace(b'\x34\xE8\x87\x40\xB9', b'\x34\x28\x02\x80\x52'),
    ('vendor/bin/mnld', 'vendor/lib64/libaalservice.so', 'vendor/lib64/libcam.utils.sensorprovider.so', 'vendor/lib64/liboplus_mtkcam_lightsensorprovider.so'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/hw/audio.primary.mt6785.so': blob_fixup()
        .replace_needed('libalsautils.so', 'libalsautils-v31.so'),
    ('vendor/lib64/libcodec2_mtk_vdec.so', 'vendor/lib64/libcodec2_mtk_venc.so'): blob_fixup()
        .replace_needed(
            'vendor.oplus.hardware.performance-V1-ndk_platform.so',
            'vendor.oplus.hardware.performance-V1-ndk.so',
        ),
    'vendor/lib64/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    ('vendor/lib64/lib3a.flash.so', 'vendor/lib64/lib3a.ae.stat.so', 'vendor/lib64/lib3a.sensors.color.so', 'vendor/lib64/lib3a.sensors.flicker.so', 'vendor/lib64/libaaa_ltm.so'): blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so')
        # Preserve PictureQuality threadLoop x25 on the PQ fallback path.
        # Without this, x25 becomes NULL and CCORR crashes reading [x25 + 0x90].
        .binary_regex_replace(
            b'\x21\xff\xff\x90\x02\xff\xff\xf0\x21\xfc\x0a\x91\x42\x48\x39\x91',
            b'\x09\xff\x91\x52\x49\x00\xa0\x72\x79\x03\x09\x8b\x07\x01\x00\x14',
        )
        .binary_regex_replace(
            b'\xe0\x03\x1b\xaa\xcd\x74\x00\x94\x76\x13\x00\x36\x21\xff\xff\x90',
            b'\xe0\x03\x1b\xaa\xcd\x74\x00\x94\x36\xf2\x07\x36\x21\xff\xff\x90',
        ),
    ('vendor/lib/libnvram.so', 'vendor/lib64/libnvram.so', 'vendor/lib64/libsysenv.so', 'vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron'): blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib64/hw/hwcomposer.mt6785.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so')
}  # fmt: skip

module = ExtractUtilsModule(
    'nashc',
    'realme',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
