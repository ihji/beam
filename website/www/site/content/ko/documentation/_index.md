---
title: "Learn about Beam"
aliases:
  - /learn/
  - /docs/learn/
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

# 아파치 빔 도움말

이 문서에서는 빔 모델, 개발 도구, 그리고 실행기들에 대해 자세한 개념을 제시하고 참고가 될만한 자료들을 다룹니다.

## 기본 개념 배우기

빔 프로그래밍 모델과 모든 빔 개발 도구와 실행기들에 적용 가능한 기본 개념들을 배웁니다.

* 빔에서 중요한 개념들을 상세하게 소개하는 [프로그래밍 가이드](/ko/documentation/programming-guide/)를 읽어보세요.
* 파이프라인이 어떻게 실행되는지 더 잘 이해하기 위해 빔의 [실행 모델](/ko/documentation/runtime/model)에 대해 배울 수 있습니다.
* [학습 자료](/ko/documentation/resources/learning-resources)를 방문하여 빔에 대한 유용한 글들과 발표들을 볼 수 있습니다.

## 파이프라인의 기초

* [파이프라인 디자인하기](/ko/documentation/pipelines/design-your-pipeline/): 파이프라인의 구조를 설계하고 데이터에 적용할 변환기들을 고르며 입력과 출력 방법을 결정합니다.
* [파이프라인 작성하기](/ko/documentation/pipelines/create-your-pipeline/): 빔 개발 도구에서 제공하는 클래스들을 이용해 보세요.
* [파이프라인 테스트하기](/ko/documentation/pipelines/test-your-pipeline/): 파이프라인을 원격으로 실행할 때 발생할 수 있는 문제를 최소화 합니다.

## 개발 도구들

사용 가능한 개발 도구들의 현재 개발 상황과 참고가 될 만한 다른 정보들을 찾아보세요.

* [자바 개발 도구](/documentation/sdks/java/)
* [파이썬 개발 도구](/documentation/sdks/python/)
* [고 개발 도구](/documentation/sdks/go/)

## 실행기들

빔 실행기는 빔 파이프라인을 특정한 데이터 처리 시스템 (대부분의 경우 분산 처리를 지원하는) 에서 실행합니다.

### 사용 가능한 실행기들

* [DirectRunner](/documentation/runners/direct/): 로컬 머신에서 실행 -- 개발과 테스팅 그리고 디버깅에 적합합니다.
* [FlinkRunner](/documentation/runners/flink/): [아파치 플링크](https://flink.apache.org)에서 실행합니다.
* [SparkRunner](/documentation/runners/spark/): [아파치 스파크](https://spark.apache.org)에서 실행합니다.
* [DataflowRunner](/documentation/runners/dataflow/): [구글 클라우드 데이터플로우](https://cloud.google.com/dataflow)에서 실행합니다. [구글 클라우드 플랫폼](https://cloud.google.com/)이 제공하는 완전 관리형 서비스입니다.
* [SamzaRunner](/documentation/runners/samza/): [아파치 삼자](https://samza.apache.org)에서 실행합니다.
* [NemoRunner](/documentation/runners/nemo/): [아파치 네모](https://nemo.apache.org)에서 실행합니다.
* [JetRunner](/documentation/runners/jet/): [헤이즐캐스트 젯](https://jet.hazelcast.org/)에서 실행합니다.

### 실행기 선택하기

빔은 파이프라인을 여러개의 다른 실행기에서 실행 가능하도록 디자인 되었습니다. 하지만 각각의 실행기가 제공하는 기능의 차이 때문에 빔 모델의 핵심적인 개념들이 모든 실행기에서 동일하게 사용 가능하지는 않습니다. [기능 비교표](/documentation/runners/capability-matrix/)를 참고하면 각각의 실행기가 제공하는 기능에 대해 자세히 비교해 볼 수 있습니다. 

어떤 실행기를 사용할지 고르고 나면, 그 실행기의 설명 페이지를 참고하여 실행기를 처음으로 사용가능하도록 준비하는 법과 실행에 필요한 필수적인 또는 선택적인 파이프라인 옵션(`PipelineOptions`)에 대한 정보를 얻을 수 있습니다. 단어세기(`WordCount`) 예제 파이프라인을 실행하는 방법을 알고 싶다면 [자바](/get-started/quickstart-java), [파이썬](/get-started/quickstart-py) 또는 [고](/get-started/quickstart-go) 개발 도구의 빠르게 시작하기 문서를 참고하세요.
