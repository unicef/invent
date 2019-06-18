<template>
  <div class="DHAHelpCenter">
    <div class="PageTitle">
      <h2><translate>DHA Help Center</translate></h2>
      <el-button
        type="text"
        class="Back IconLeft"
        @click="goBack"
      >
        <fa icon="angle-left" />
        <translate>Go back</translate>
      </el-button>
    </div>

    <el-card
      :body-style="{ padding: '0px' }"
      class="HelpCard"
    >
      <el-tabs tab-position="left">
        <el-tab-pane :label="$gettext('Terms of Use') | translate">
          <h2><translate>Terms of Use</translate></h2>
          <p>
            <translate>
              Please read these Terms of Use before using the Website or any of its features. By using the
              Website, you accept and agree to be bound by these Terms. If you do not agree to the Terms,
              please exit the Website and do not access or otherwise use the Website.
            </translate>
          </p>
          <p>
            <translate>The following Terms of Use (“Terms”) govern the use of</translate>
            <a
              href="http://www.digitalhealthatlas.org/"
              title="www.digitalhealthatlas.org"
            >
              www.digitalhealthatlas.org
            </a>
            <translate>
              (“Website”), including without limitation participation in its forums, blog, and all linked
              pages owned and operated by Results for Development Institute (“HRP,” “we,” or “our”).
            </translate>
          </p>
          <p>
            <translate>
              We reserve the right to modify, add, or delete any of these Terms at any time. Continued use of
              the Website after any modifications, additions, or deletions to the Terms will constitute your
              acceptance of the Terms, as modified.
            </translate>
          </p>
          <p><translate>This Site Does Not Provide Medical Advice, Diagnosis or Treatment.</translate></p>
          <p>
            <translate>
              The contents of the Website such as texts, graphics, images, and all other information, whether
              provided by HRP or its users, are for informational purposes only. The content is not intended
              to be a substitute for professional medical advice, diagnosis, or treatment. If you need
              specific advice (for example, medical, legal, or financial) please seek a professional who is
              licensed or knowledgeable in that area.
            </translate>
          </p>
          <h4><translate>Accuracy of Content</translate></h4>
          <p>
            <translate>
              The use of the Website and its content is at your own risk. HRP makes a reasonable effort to
              ensure that the content of the Website is accurate and up-to-date, but does not offer any
              warranties (whether express, implied or otherwise) as to the reliability, accuracy or
              completeness of the information appearing on the Website, whether provided by HRP or any user,
              information provider, or any other person or entity. HRP may remove material from the Website at
              its own discretion and without giving any notice.
            </translate>
          </p>
          <p>
            <translate>
              HRP, its contributors, sponsors, administrators, or anyone else connected with HRP in any way
              whatsoever, cannot be responsible for any inaccurate or libelous information or for your use of
              the information contained in or linked from these web pages.
            </translate>
          </p>
          <h4><translate>Intellectual Property Rights</translate></h4>
          <p>
            <translate>
              The contents of the Website are protected by copyright, trademark, and other intellectual
              property laws. The Website may not be used in any manner that violates the privacy rights,
              publicity rights, copyrights, trademark rights, patent rights, contract rights, or any other
              rights belonging to HRP or a third party. Unless authorized by the Terms or by the owner of the
              materials, you are strictly prohibited from modifying, copying, reproducing, republishing,
              uploading, posting, transmitting, translating, selling, creating derivative works, or
              distributing in any manner or medium (including email or other electronic means) any material
              from the Website. Your use of the Website does not grant you ownership of any content, code,
              data, or other materials you may access on or through the Website. Use of the Website and the
              services offered on or through the Website are only for your personal and non-commercial
              use.
            </translate>
          </p>
          <p>
            <translate>
              When you post or submit any material to this Website, you represent and warrant that you are the
              owner of the material or have express permission from the owner of the material to post, use, or
              submit the material. By posting or submitting material to the Website, you agree that such
              submission is non-confidential for all purposes. You are solely responsible for any damages
              resulting from any infringements of copyrights, trademark rights, propriety rights, or any other
              harm resulting from any uploading, posting, or submission. When you post or submit material to
              the Website, you grant HRP the right to use the material, royalty-free, and grant us a
              non-exclusive, perpetual, and worldwide license to use, reproduce, modify, adapt, publish,
              translate, display, distribute and create any type of derivative work from the submitted
              material. Submitting or posting material also grants us the right to identify you as the author
              of any of your postings or submissions by name, email address, or username, as we deem
              appropriate. If you wish to keep any information, ideas, concepts or inventions private or
              proprietary, do not submit them to the Website or to HRP by email. We try to answer every email
              in a timely manner, but are not always able to do so.
            </translate>
          </p>
          <p>
            <translate>
              We respect the intellectual property rights of others and require that people who use the Website
              and services available on the Website do the same. If you believe your work has been copied in a
              way that constitutes infringement, please forward the following information to our designated
              offices: • your address, telephone number, and email address; • a description of the copyrighted
              work you claim has been infringed; • a description of where the alleged infringing material is
              located; • a statement that you have a good faith belief that the disputed use is not authorized
              by the copyright owner, its agent, or the law; • an electronic or physical signature of the
              person authorized to act on behalf of the owner of the copyright interest; and • a statement by
              you, made under penalty of perjury, that the above information in your notice is accurate and
              that you are the copyright owner or are authorized to act on the copyright owner's behalf.
            </translate>
          </p>
          <h4><translate>Message Boards and Other Interactive Features</translate></h4>
          <p>
            <translate>
              Message boards, bulletin boards, blogs, and other services may be available on or through the
              Website. In addition to any other rules or regulations that HRP posts in connection with these
              particular services, you shall not upload, post, transmit, distribute, or otherwise publish
              through the Website or any service or feature made available on or through the Website any
              materials which: (a) restrict or inhibit any other user from using and enjoying the Website; (b)
              are fraudulent, unlawful, threatening, abusive, harassing, libelous, defamatory, or offensive;
              (c) constitute or encourage conduct that would constitute a criminal offense, give rise to civil
              liability or otherwise violate any local, state, federal, or international law; (d) violate,
              plagiarize, or infringe the rights of third parties, including, without limitation, copyright,
              trademark, trade secret, confidentiality, contract, patent, rights of privacy, or publicity or
              any other proprietary rights; (e) contain a virus, spyware, or any other harmful content; (f)
              contain embedded links or advertising of any kind; or (g) constitute or contain false or
              misleading indications of origin, endorsements, or statements of fact.
            </translate>
          </p>
          <p>
            <translate>
              HRP reserves the right, but has no obligation, to monitor the content of the message boards,
              bulletin boards, blogs, and other services available on the Website to determine compliance with
              the Terms of Use and any other operating rules we establish. We reserve the exclusive right to
              edit, remove, or refuse to post any submitted materials or information. We are not responsible
              for and do not endorse any of the opinions, advice, or statements posted in messages, bulletin
              boards, blogs, and other services. We are not responsible for any offensive, defamatory, or
              obscene posting made on the message boards or other features on the Website. We reserve the
              right to disclose any information we believe necessary to satisfy any Law regulation, or
              governmental request, or to refuse to post or to remove any information or materials, in whole
              or in part, that in our sole discretion are inappropriate, objectionable or in violation of
              these Terms. We also reserve the right to deny access to the Website or any features of the
              Website to anyone who violates these Terms or who, in our judgment, interferes with the ability
              of others to enjoy our website or infringes the rights of others. HRP assumes no liability for
              any action or inaction with respect to any conduct, communication, or posting on the message
              boards, bulletin boards, blogs, or other services on this Website.
            </translate>
          </p>
          <h4><translate>Privacy Policy</translate></h4>
          <p>
            <translate>
              We know that you care how information about you is used and shared and we are careful to ensure
              that any such information that comes into our possession is properly looked after. This Privacy
              Policy sets out the steps that we take to ensure that any information provided to us is kept
              secure and confidential and is used only for the purposes for which it is provided.
            </translate>
          </p>
          <h4><translate>Personal Information</translate></h4>
          <p>
            <translate>
              The only personal information that we will collect is the personal information that you provide
              to us when you register with us or when you communicate with us through our website. We will at
              any time, at your request, provide you with a copy of any personal information that we are
              holding about you.
            </translate>
          </p>
          <h4><translate>Purposes for which Personal Information May Be Used</translate></h4>
          <p><translate>Any personal information that you provide to us will be used only for the following purposes:</translate></p>
          <ul>
            <li><translate>To provide information or services to you as requested by you.</translate></li>
            <li><translate>To let you know about information and services from HRP in which you may be interested.</translate></li>
            <li><translate>For internal review.</translate></li>
            <li><translate>To improve the content of the website.</translate></li>
            <li><translate>To customize the content and /or layout of the website for each individual user.</translate></li>
            <li><translate>To notify users about updates to the website.</translate></li>
            <li>
              <translate>
                To compile and disclose statistics about our users and their preferences. However, these
                statistics are anonymous and do not identify individual users.
              </translate>
            </li>
          </ul>
          <h4><translate>Disclosure</translate></h4>
          <p>
            <translate>
              We will not pass any of your personal information to any third party, other than members of HRP,
              without your consent.
            </translate>
          </p>
          <h4><translate>Marketing and Advertising</translate></h4>
          <p>
            <translate>
              No promotional offers or advertising will appear on the Website nor will your personal contact
              information ever be given, sold, or otherwise shared by HRP with third parties for advertising
              or marketing purposes.
            </translate>
          </p>
          <h4><translate>Third Party Sites</translate></h4>
          <p>
            <translate>
              You may be able to link from HRP's Website to third-party websites; conversely, third-party
              websites may link to HRP’s Website. You acknowledge and agree that HRP's Website has no
              responsibility for the information, content, products, services, advertising, code, or other
              materials which may be provided by or through third-party sites. Links to third-party sites do
              not constitute an endorsement or sponsorship by HRP's Website of such third-party sites or the
              information, content, products, services, advertising, or other materials presented on or
              through such websites. You agree that HRP and its affiliates are not responsible for any damages
              that you incur arising from your use of any products or services made available by third-parties
              through the Website.
            </translate>
          </p>
          <h4><translate>Registration and Passwords</translate></h4>
          <p>
            <translate>
              To access certain services of the Website, you may need to provide information such as your name,
              email address, street address, and zip code. By use of these services, you agree to: (a) provide
              accurate, current, and complete information about you; (b) maintain the security of your
              password and identification; (c) maintain and promptly update your data and any other
              information you provide to the Website to keep it accurate, current, and complete; and (d) be
              fully responsible for all use of your account and for any actions, whether by you or another
              person, that take place using your account. You will notify us immediately of any unauthorized
              use of your password or account or any other breach of security. HRP assumes no liability for
              any loss or damage arising from any unauthorized use of your password or account by a third
              party. Any reliance on the contents of a third-party site is done at your own risk and you
              assume all responsibilities and consequences resulting from such reliance. Our use of any
              personally identifiable information provided by you in regards to obtaining a registration and
              password is governed by the terms of our Privacy Policy.
            </translate>
          </p>
          <h4><translate>Disclaimers</translate></h4>
          <p>
            <translate>
              This Website provides links to websites maintained by third parties. Any information, products,
              or services provided by the third-party sites are maintained by the operators of such sites and
              not by HRP or our subsidiaries. When these third-party sites are accessed, they are accessed at
              your own risk.
            </translate>
          </p>
          <p><translate>The Website and any content, materials, features, or products available or sold on or through the Website are available on an “as is” basis.</translate></p>
          <p>
            <small>
              <translate>
                HRP, TO THE FULLEST EXTENT PERMITTED BY LAW,
                DISCLAIMS ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF
                TITLE, NON-INFRINGEMENT OF THIRD PARTIES’ RIGHTS, AND IMPLIED WARRANTIES OF MERCHANTABILITY OF
                FITNESS FOR A PARTICULAR PURPOSE. HRP DOES NOT WARRANT THAT THIS SERVICE WILL BE UNINTERRUPTED
                OR ERROR-FREE, VIRUS-FREE, NOR DOES HRP MAKE ANY WARRANTIES THAT ANY DEFECTS WILL BE
                CORRECTED.
              </translate>
            </small>
          </p>
          <p>
            <small>
              <translate>
                WE MAKE NO WARRANTY THAT THE WEBSITE OR THE PROVIDED SERVICES WILL MEET USERS' REQUIREMENTS. NO
                ADVICE, RESULTS OR INFORMATION, WHETHER ORAL OR WRITTEN, OBTAINED BY YOU FROM US OR THROUGH THE
                WEBSITE SHALL CREATE ANY WARRANTY NOT EXPRESSLY MADE HEREIN. HRP ALSO ASSUMES NO RESPONSIBILITY,
                AND SHALL NOT BE LIABLE FOR, ANY DAMAGES TO, OR VIRUSES THAT MAY INFECT, YOUR EQUIPMENT ON
                ACCOUNT OF YOUR ACCESS TO, USE OF, OR BROWSING IN THE WEBSITE OR YOUR DOWNLOADING OF ANY
                MATERIALS, DATA, TEXT, IMAGES, VIDEO CONTENT, OR AUDIO CONTENT FROM THE WEBSITE. IF YOU ARE
                DISSATISFIED WITH THE WEBSITE, YOUR SOLE REMEDY IS TO DISCONTINUE USING THE WEBSITE.
              </translate>
            </small>
          </p>
          <p>
            <small>
              <translate>
                WE TRY TO ENSURE THAT THE INFORMATION POSTED ON THE WEBSITE IS CORRECT AND UP-TO-DATE. WE RESERVE
                THE RIGHT TO CHANGE OR MAKE CORRECTIONS TO ANY OF THE INFORMATION PROVIDED ON THE WEBSITE AT ANY
                TIME AND WITHOUT ANY PRIOR WARNING. HRP NEITHER ENDORSES NOR IS RESPONSIBLE FOR THE ACCURACY OR
                RELIABILITY OF ANY OPINION, ADVICE OR STATEMENT ON THE WEBSITE, NOR FOR ANY OFFENSIVE,
                DEFAMATORY, OBSCENE, INDECENT, UNLAWFUL OR INFRINGING POSTING MADE THEREON BY ANYONE OTHER THAN
                AUTHORIZED HRP EMPLOYEE SPOKESPERSONS WHILE ACTING IN THEIR OFFICIAL CAPACITIES (INCLUDING,
                WITHOUT LIMITATION, OTHER USERS OF THE WEBSITE). IT IS YOUR RESPONSIBILITY TO EVALUATE THE
                ACCURACY, COMPLETENESS OR USEFULNESS OF ANY INFORMATION, OPINION, ADVICE OR OTHER CONTENT
                AVAILABLE THROUGH THE WEBSITE. PLEASE SEEK THE ADVICE OF PROFESSIONALS, AS APPROPRIATE,
                REGARDING THE EVALUATION OF ANY SPECIFIC INFORMATION, OPINION, ADVICE OR OTHER CONTENT,
                INCLUDING BUT NOT LIMITED TO FINANCIAL, HEALTH, OR LIFESTYLE INFORMATION, OPINION, ADVICE OR
                OTHER CONTENT.
              </translate>
            </small>
          </p>
          <h4><translate>Limitations on Liability</translate></h4>
          <p>
            <translate>
              In no event will HRP or its directors, employees, or agents be liable to you or any third person
              for any direct, indirect, consequential, exemplary, incidental, special, or punitive damages,
              including for any lost profits or lost data arising from your use of the Website or this service
              or the unavailability of the Website or this service. When using the Website, information will
              be transmitted over a medium that may be beyond the control and jurisdiction of HRP.
              Accordingly, HRP assumes no liability for or relating to the delay, failure, interruption, or
              corruption of any data or other information transmitted in connection with use of the
              Website.
            </translate>
          </p>
          <h4><translate>Terminations</translate></h4>
          <p>
            <translate>
              At any time and without notice, we may suspend, cancel, or terminate your right to use this
              Website or any portion of the Website. In the event of a suspension, cancellation, or
              termination, you are no longer authorized to access the part of the Website affected by such
              suspension, cancellation, or termination.
            </translate>
          </p>
          <h4><translate>Other Terms</translate></h4>
          <p>
            <translate>
              These Terms constitute the entire agreement between you and HRP regarding the use of the Website
              and supersede any prior agreements between you and HRP relating to your use of the Website. The
              failure of HRP to exercise or enforce any right or provision of these Terms shall not constitute
              a waiver of such right or provision in that or any other instance. If any provision of these
              Terms is held invalid, the remainder of the Terms shall continue in full force and effect. If
              any provision of these Terms shall be deemed unlawful, void, or for any other reason
              unenforceable, then that provision shall be deemed severable from these Terms and shall not
              affect the validity and enforceability of any remaining provisions. This agreement shall be
              governed and construed by the laws of the District of Columbia without giving effect to any
              principles of conflicts of law. The foregoing provisions of these Terms are for the benefit of
              HRP, its affiliates, and third-party content providers and licensors, and each shall have the
              right to asset and enforce provisions of the Terms directly and on their own behalf.
            </translate>
          </p>
        </el-tab-pane>

        <el-tab-pane :label="$gettext('Contact') | translate">
          <h2>
            <translate>Contact</translate>
          </h2>
          <p><translate>If you have further questions about the DHA, do not hesitate to get in touch using the details below:</translate></p>
          <p>
            <b><translate>Email:</translate></b>&nbsp;<a href="mailto:digitalhealthatlas@gmail.com">
              digitalhealthatlas@gmail.com
            </a>
          </p>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  methods: {

    goBack () {
      this.$router.go(-1);
    }
  }
};
</script>

<style lang="less">
@import "~assets/style/variables.less";
@import "~assets/style/mixins.less";

.DHAHelpCenter {

  .HelpCard {
    width: @cardSizeMedium;
    margin: 0 auto 80px;

    .el-tabs {
      .el-tabs__header {
        margin: 30px 0 0;

        .el-tabs__nav {
          .el-tabs__item {
            padding: 0 30px;
            color: @colorTextSecondary;

            &:hover {
              color: @colorTextPrimary;
            }

            &.is-active {
              color: @colorBrandPrimary;
            }
          }
        }
      }

      .el-tabs__content {
        padding: 20px 60px 80px;
        transform: translateX(-1px);
        box-shadow: inset 2px 0 0 0 @colorGrayLightest;

        p,
        li {
          font-size: @fontSizeBase;
          line-height: 19px;

          a {
            color: @colorBrandPrimary;

            &:hover {
              text-decoration: none;
            }
          }
        }

        .el-button {
          margin: 10px 0;
        }
      }
    }
  }

  .GetToolkit {}
}
</style>
