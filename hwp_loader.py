"""
HWP 파일에서 텍스트를 추출하는 모듈
HWP 5.0 (OLE2) 및 HWPX (XML/ZIP) 지원
"""
import zipfile
import xml.etree.ElementTree as ET

def get_hwp_text(filename):
    """
    HWP 파일에서 텍스트를 추출합니다.
    1차: HWPX (ZIP) 시도
    2차: HWP 5.0 (OLE2) 시도
    3차: pyhwp 시도
    """
    # 1차: HWPX 형식 시도
    try:
        text = get_hwpx_text(filename)
        if text:
            print(f"✓ HWPX로 추출 성공: {len(text)} 글자")
            return text
    except Exception as e:
        print(f"HWPX 실패: {e}")

    # 2차: HWP 5.0 (OLE2) 시도
    try:
        text = get_hwp5_text(filename)
        if text:
            print(f"✓ HWP5로 추출 성공: {len(text)} 글자")
            return text
    except Exception as e:
        print(f"HWP5 실패: {e}")

    # 3차: pyhwp 시도
    try:
        text = get_hwp_pyhwp(filename)
        if text:
            print(f"✓ pyhwp로 추출 성공: {len(text)} 글자")
            return text
    except Exception as e:
        print(f"pyhwp 실패: {e}")

    print(f"✗ 모든 방법 실패: {filename}")
    return ""


def get_hwpx_text(filename):
    """
    HWPX (HWP 2014+) 파일에서 텍스트 추출
    ZIP 파일 내부의 XML 파싱
    """
    text_parts = []

    with zipfile.ZipFile(filename, 'r') as zf:
        file_list = zf.namelist()
        print(f"ZIP 파일 내용: {file_list[:5]}...")  # 처음 5개만

        # Contents 폴더 내의 section*.xml 파일들 찾기
        section_files = [f for f in file_list if 'section' in f.lower() and f.endswith('.xml')]

        if not section_files:
            raise Exception(f"section XML 파일을 찾을 수 없음. 파일 목록: {file_list[:10]}")

        print(f"섹션 파일: {section_files}")

        for section_file in sorted(section_files):
            xml_content = zf.read(section_file)
            root = ET.fromstring(xml_content)

            # 모든 텍스트 노드 추출
            for text_elem in root.iter():
                if text_elem.text and text_elem.text.strip():
                    text_parts.append(text_elem.text.strip())
                if text_elem.tail and text_elem.tail.strip():
                    text_parts.append(text_elem.tail.strip())

    if not text_parts:
        raise Exception("XML에서 텍스트를 찾을 수 없음")

    return ' '.join(text_parts)


def get_hwp5_text(filename):
    """
    HWP 5.0 (OLE2) 파일에서 텍스트 추출
    """
    import olefile
    import zlib

    f = olefile.OleFileIO(filename)
    dirs = f.listdir()

    print(f"OLE2 디렉토리: {dirs[:5]}...")

    if ["FileHeader"] not in dirs:
        f.close()
        raise Exception("FileHeader가 없음 - HWP 5.0 파일이 아님")

    sections = sorted([d[1] for d in dirs if d[0] == "BodyText"])
    print(f"BodyText 섹션: {sections}")

    if not sections:
        f.close()
        raise Exception("BodyText 섹션이 없음")

    text_parts = []

    for section in sections:
        bodytext = f.openstream("BodyText/" + section).read()

        # zlib 압축 해제
        try:
            unpacked_data = zlib.decompress(bodytext, -15)
        except:
            unpacked_data = bodytext

        # UTF-16LE로 디코딩
        decoded = unpacked_data.decode('utf-16le', errors='ignore')

        # 출력 가능한 문자만 추출
        clean_text = ''.join(
            c for c in decoded
            if c.isprintable() or c in '\n\r\t '
        )

        if clean_text.strip():
            text_parts.append(clean_text.strip())

    f.close()

    if not text_parts:
        raise Exception("텍스트를 추출할 수 없음")

    return '\n'.join(text_parts)


def get_hwp_pyhwp(filename):
    """
    pyhwp 라이브러리 사용
    """
    from hwp5.xmlmodel import Hwp5File
    from io import StringIO

    hwp = Hwp5File(filename)
    text_parts = []

    for section in hwp.bodytext.section_iterator():
        text_stream = StringIO()
        section.plaintext(text_stream)
        text = text_stream.getvalue()
        if text.strip():
            text_parts.append(text.strip())

    hwp.close()

    if not text_parts:
        raise Exception("pyhwp에서 텍스트를 찾을 수 없음")

    return '\n'.join(text_parts)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = get_hwp_text(sys.argv[1])
        print(f"\n추출된 텍스트 길이: {len(text)}")
        if text:
            print("\n처음 500자:")
            print(text[:500])

            # 육아휴직 검색
            if '육아' in text or '휴직' in text:
                print("\n✓ '육아' 또는 '휴직' 키워드 발견!")
