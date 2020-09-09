---
title: "빔 살펴보기"
aliases:
  - /use/beam-overview/
  - /docs/use/beam-overview/
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

# 아파치 빔 살펴보기

아파치 빔은 배치와 스트리밍 데이터 처리 파이프라인을 하나로 표현 할 수 있는 통합된 오픈소스 파이프라인 모델입니다. 오픈소스 빔 개발 도구 중 하나를 사용하여 파이프라인을 정의 합니다. 정의된 파이프라인은 빔이 지원하는 **분산 처리 엔진** 중 하나를 선택하여 실행하게 됩니다. 빔이 지원하는 대표적인 분산 처리 엔진으로는 [아파치 플링크](https://flink.apache.org), [아파치 스파크](http://spark.apache.org), 그리고 [구글 클라우드 데이터플로우](https://cloud.google.com/dataflow) 등이 있습니다.

빔은 [무자비하게 병렬적인](https://en.wikipedia.org/wiki/Embarassingly_parallel) 데이터 처리 업무에 특별히 유용합니다. 이런 업무들은 데이터를 수많은 작은 꾸러미로 쪼갤 수 있으며 쪼개진 꾸러미는 독립적이고 병렬적으로 처리 가능한 특징이 있습니다. 빔은 또한 추출, 변환, 적재 (Extract, Transform, Load: ETL) 업무나 순수한 데이터 통합작업에 사용되는데, 빔을 사용하면 데이터를 다른 저장소와 소스사이에 이동 시킬 수 있고 원하는 형태로 변환 할 수 있으며 완전히 새로운 시스템에 쉽게 이전하는 것도 가능합니다.

## 아파치 빔 개발 도구

아파치 빔 개발 도구를 사용하면 데이터의 크기가 크든 작든, 한정된 배치 데이터 소스를 처리하든 무한한 스트리밍 데이터 소스를 처리하든 동일한 통합 프로그래밍 모델로 파이프라인을 나타낼 수 있습니다. 빔 개발 도구는 유한하거나 무한함과 상관 없이 동일한 클래스를 사용하여 데이터를 표현하며, 동일한 변환기를 사용하여 데이터를 처리합니다. 사용자는 취향에 맞는 빔 개발 도구를 골라 자신의 데이터 처리 파이프라인을 정의하는 프로그램을 만들게 됩니다.

빔 개발 도구는 현재 다음과 같은 프로그래밍 언어를 지원합니다:

- 자바 ![Java logo](/images/logos/sdks/java.png)
- 파이썬 ![Python logo](/images/logos/sdks/python.png)
- 고 <img src="/images/logos/sdks/go.png" height="45px" alt="Go logo">

스칼라 <img src="/images/logos/sdks/scala.png" height="45px" alt="Scala logo"> 를 사용하기 원하는 경우 [Scio](https://github.com/spotify/scio)가 있습니다.

## 아파치 빔 파이프라인 실행기

빔 파이프라인 실행기는 사용자가 빔 프로그램을 통해 정의한 데이터 처리 파이프라인을 다양한 분산 처리 백엔드와 호환 가능한 API로 번역합니다. 사용자가 빔 프로그램을 실행 할 때 [적당한 실행기](/documentation/runners/capability-matrix)를 지정하여 어떤 백엔드에서 파이프라인을 실행하기 원하는지 선택합니다.

빔의 실행기들은 현재 다음과 같은 분산 처리 백엔드를 지원합니다:

- 아파치 플링크 ![Apache Flink logo](/images/logos/runners/flink.png)
- 아파치 삼자 <img src="/images/logos/runners/samza.png" height="20px" alt="Apache Samza logo">
- 아파치 스파크 ![Apache Spark logo](/images/logos/runners/spark.png)
- 구글 클라우드 데이터플로우 ![Google Cloud Dataflow logo](/images/logos/runners/dataflow.png)
- 헤이즐캐스트 젯 ![Hazelcast Jet logo](/images/logos/runners/jet.png)

**참고:** 잊지마세요! 테스팅과 디버깅을 위해 언제든 로컬 머신에서도 실행 가능합니다.

## 시작하기

빔을 이용해 데이터 처리 업무를 시작해봅시다.

1. 웹 브라우저에서 상호작용 환경을 만들어 [아파치 빔 해보기](/ko/get-started/try-apache-beam).

1. [자바 개발 도구](/ko/get-started/quickstart-java), [파이썬 개발 도구](/ko/get-started/quickstart-py) 또는 [고 개발 도구](/ko/get-started/quickstart-go)의 빠르게 시작하기 문서를 따라해 봅니다.

1. 개발 도구의 다양한 기능에 대해 소개하는 [단어세기 예제 따라잡기](/ko/get-started/wordcount-example)를 읽어 봅니다.

1. [학습 자료](/ko/documentation/resources/learning-resources)를 통해 자습 할 수 있습니다.

1. [개발 문서](/ko/documentation/)를 정독하여 빔 모델, 개발 도구, 실행기에 대한 깊은 지식을 얻을 수 있습니다.

## 기여하기

빔은 아파치 v2 라이센스로 제공되는 <a href="http://www.apache.org" target="_blank">아파치 소프트웨어 재단</a>의 프로젝트 입니다. 빔은 오픈소스로 개발되고 있으며 모든 기여자 분들을 환영합니다! 프로젝트에 기여하고 싶으시다면 [기여하기](/ko/contribute/)에서 시작하세요.
