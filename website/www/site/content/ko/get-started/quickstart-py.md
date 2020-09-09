---
title: "빔 파이썬 빠르게 시작하기"
---
<!--
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# 아파치 빔 파이썬 개발 도구 빠르게 시작하기

이 가이드는 파이썬 개발 환경을 구성하는 법과 아파치 빔 파이썬 개발 도구를 설치하는 방법 그리고 예제 파이프라인을 실행하는 방법에 대하여 다룹니다.

아파치 빔 파이썬 개발 도구의 개발에 기여하고 싶으시다면 [기여하기 가이드](/ko/contribute)를 읽어보세요!

{{< toc >}}

파이썬 개발 도구는 파이썬 2.7, 3.5, 3.6, 3.7을 지원합니다. 2020년 중 새로 릴리즈 되는 파이썬 개발 도구에서는 파이썬 2.7에 대한 지원이 중단될 예정입니다 ([BEAM-8371](https://issues.apache.org/jira/browse/BEAM-8371)). 빔 프로그램을 새로 작성하실 경우 파이썬 3를 사용해주세요.

## 환경 설정

### 파이썬 버전 확인하기

빔 개발 도구는 파이썬 2 사용자의 경우 파이썬 2.7을 파이썬 3 사용자의 경우 파이썬 3.5 또는 그 이상 버전을 요구합니다. 다음을 실행하여 파이썬 버전을 확인하세요:

{{< highlight >}}
python --version
{{< /highlight >}}

### pip 설치하기

파이썬 패키지 매니저 [pip](https://pip.pypa.io/en/stable/installing/)를 설치합니다. 다음을 실행하여 7.0.0 이상의 버전이 설치되었는지 확인합니다:

{{< highlight >}}
pip --version
{{< /highlight >}}

만약 `pip` 버전이 7.0.0 이상이 아니라면 다음 명령어를 실행하여 업그레이드 합니다. 관리자 권한이 필요할 수도 있습니다.

{{< highlight class="shell-unix" >}}
pip install --upgrade pip
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> python -m pip install --upgrade pip
{{< /highlight >}}


### 파이썬 가상 환경 설치하기

여러 구성을 자유롭게 실험해보기 위해 [파이썬 가상 환경](https://docs.python-guide.org/en/latest/dev/virtualenvs/)을 설치하기를 권장합니다. `virtualenv` 버전 13.1.0 이상이 설치되어 있지 않다면 다음을 실행하여 업그레이드 합니다. 관리자 권한이 필요할 수도 있습니다.

{{< highlight class="shell-unix" >}}
pip install --upgrade virtualenv
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> python -m pip install --upgrade virtualenv
{{< /highlight >}}

파이썬 가상 환경을 사용하기 원하지 않는다면 (추천하지 않습니다) `setuptools`가 설치되어 있는지 확인합니다. `setuptools` 버전 17.1 이상이 설치되어 있지 않다면 다음 명령어를 실행하여 설치합니다.

{{< highlight class="shell-unix" >}}
pip install --upgrade setuptools
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> python -m pip install --upgrade setuptools
{{< /highlight >}}

## 아파치 빔 설치하기

### 가상 환경을 만들고 활성화 시키기

가상 환경은 독립적인 파이썬 배포판을 포함하는 디렉토리 구조를 가집니다. 가상 환경을 생성하기 위해서는 새로운 디렉토리를 만들고 다음을 실행합니다:

{{< highlight class="shell-unix" >}}
virtualenv /path/to/directory
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> virtualenv C:\path\to\directory
{{< /highlight >}}

가상 환경은 사용이 필요할 때마다 각각의 쉘에서 활성화 되어야 합니다. 활성화 하면 가상 환경이 생성된 디렉토리를 가리키는 몇개의 환경 변수가 설정 됩니다.

배쉬 쉘에서 가상 환경을 활성화 하려면 다음을 실행하세요:

{{< highlight class="shell-unix" >}}
. /path/to/directory/bin/activate
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> C:\path\to\directory\Scripts\activate.ps1
{{< /highlight >}}

이 명령어는 만들어진 가상 환경 디렉토리 안의 `activate` 스크립트를 실행합니다.

다른 쉘을 사용 할 경우 [virtualenv 문서](https://virtualenv.pypa.io/en/stable/userguide/#activate-script)를 참조해 주세요.

### 다운로드와 설치

PyPI에서 최신 파이썬 개발 도구를 설치합니다:

{{< highlight class="shell-unix" >}}
pip install apache-beam
{{< /highlight >}}

{{< highlight class="shell-PowerShell" >}}
PS> python -m pip install apache-beam
{{< /highlight >}}

#### 추가 요구사항

앞서 설명된 설치 방법은 구글 클라우드 데이터플로우 실행기와 같은 추가적인 의존 패키지들을 함께 설치하지 않습니다. 어떤 기능이 어떤 추가 패키지들을 필요로 하는지는 아래에 설명되어 있습니다. `pip install apache-beam[feature1,feature2]`와 같은 명령을 사용하여 한꺼번에 여러개의 추가적인 의존 패키지들을 설치 할 수 있습니다.

- **구글 클라우드 플랫폼**
  - 설치 명령어: `pip install apache-beam[gcp]`
  - 다음 기능을 사용하기 위해 필요함:
    - 구글 클라우드 데이터플로우 실행기
    - GCS IO
    - Datastore IO
    - BigQuery IO
- **아마존 웹 서비스**
  - 설치 명령어: `pip install apache-beam[aws]`
  - AWS와 통신하기 위해 필요한 I/O 모듈을 설치합니다
- **테스트**
  - 설치 명령어: `pip install apache-beam[test]`
  - 빔 프로그램을 개발하고 단위 테스트를 실행하기 위해 필요합니다
- **문서**
  - 설치 명령어: `pip install apache-beam[docs]`
  - Sphinx를 이용하여 API 문서를 생성하기 위해 필요합니다

## 파이프라인 실행하기

아파치 빔의 [examples](https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples) 디렉토리는 많은 예제들을 포함하고 있습니다. 모든 예제 파이썬 스크립트는 파일 안에 설명된 필수 옵션을 지정하여 로컬 머신에서 실행해 볼 수 있습니다.

예를 들어 `wordcount.py`는 다음 명령어로 실행합니다:

{{< highlight class="runner-direct" >}}
python -m apache_beam.examples.wordcount --input /path/to/inputfile --output /path/to/write/counts
{{< /highlight >}}

{{< highlight class="runner-flink" >}}
python -m apache_beam.examples.wordcount --input /path/to/inputfile \
                                         --output /path/to/write/counts \
                                         --runner FlinkRunner
{{< /highlight >}}

{{< highlight class="runner-spark" >}}
python -m apache_beam.examples.wordcount --input /path/to/inputfile \
                                         --output /path/to/write/counts \
                                         --runner SparkRunner
{{< /highlight >}}

{{< highlight class="runner-dataflow" >}}
# 구글 클라우드 플렛폼 의존 패키지가 함께 설치 되어 있어야 합니다. 다음 링크를 참고하여
# 필요한 설정이 완료 되었는지 확인해주세요 /documentation/runners/dataflow/#setup
pip install apache-beam[gcp]
python -m apache_beam.examples.wordcount --input gs://dataflow-samples/shakespeare/kinglear.txt \
                                         --output gs://<your-gcs-bucket>/counts \
                                         --runner DataflowRunner \
                                         --project your-gcp-project \
                                         --region your-gcp-region \
                                         --temp_location gs://<your-gcs-bucket>/tmp/
{{< /highlight >}}

파이프라인 실행이 완료되고 나면 지정된 출력 위치에서 출력 파일들을 볼 수 있습니다. 예를 들어 `--output` 파라미터로 `/dir1/counts`를 지정했다면 파이프라인은 `/dir1/` 디렉토리에 `counts-0000-of-0001` 형식으로 된 출력 파일을 차례대로 생성합니다.

## 다음 할일들

* [빔 파이썬 개발 도구](/ko/documentation/sdks/python/)에 대하여 더 알아보고 [파이썬 개발 도구 API 사전](https://beam.apache.org/releases/pydoc)을 훑어 봅니다.
* [단어세기 예제 따라잡기](/ko/get-started/wordcount-example)를 통해 단어세기 예제에 대하여 알아봅니다.
* [학습 자료](/ko/documentation/resources/learning-resources)를 통해 자습에 필요한 정보를 얻습니다.
* 재미있는 [비디오와 팟캐스트](/ko/documentation/resources/videos-and-podcasts)들을 시청합니다.
* 빔 유저([users@](/ko/community/contact-us)) 메일링 리스트에 참여합니다.

아파치 빔을 사용하다 문제에 맞닥뜨렸다면 주저하지 말고 [연락](/ko/community/contact-us) 주세요!
